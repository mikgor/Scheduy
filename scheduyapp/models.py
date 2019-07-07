from django.db import models
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import pytz
from django.utils.translation import ugettext_lazy as _
from .classes.messengerApiHandler import MessengerApiHandler

class TaskGroup(models.Model):
    name = models.CharField(_('Name'),max_length=40)
    color = models.CharField(_('Color'),max_length=30, default="whitesmoke")
    orderIndex = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    def initializeOrderIndex(self, previousGroup):
        if previousGroup:
            self.orderIndex = previousGroup.orderIndex + 1
        else:
            self.orderIndex = 1
        self.save()

    def setOrderIndex(self, userGroups):
        previouGroup = self
        for group in userGroups:
            if group.id == self.id and not (previouGroup.id == self.id):
                currentIndex = self.orderIndex
                self.orderIndex = previouGroup.orderIndex
                previouGroup.orderIndex = currentIndex
                self.save()
                previouGroup.save()
                break
            previouGroup = group

class Notification(models.Model):
    recipient_user_id = models.IntegerField()
    details = models.CharField(_('Details'), max_length=150, blank=True)
    notification_time = models.DateTimeField(_('Notification time'), null=False)
    sent = models.BooleanField(default=False)

    def Send(self):
        AppUser.objects.get(id=self.recipient_user_id).NewNotificaton(self)

    def timeLeft(self):
        now = datetime.now(timezone.utc)
        return now >= self.notification_time

class Task(models.Model):
    name = models.CharField(_('Name'), max_length=40)
    details = models.CharField(_('Details'), max_length=150, blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(_('Deadline'), null=True, blank=True)
    priority = models.PositiveSmallIntegerField(_('Priority'), default=1)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, verbose_name = _('Group'))
    notification_time = models.DateTimeField(_('Notification time'), null=True, blank=True)
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, verbose_name = _('Notification'), null=True, blank=True)

    def __str__(self):
        return self.name

    def isExpired(self):
        now = datetime.now(timezone.utc)
        return now > self.deadline

    def remainingTime(self):
        secondsTotal = 0
        days = 0
        hours = 0
        mins = 0
        now = datetime.now(pytz.timezone('UTC'))
        secondsTotal = (self.deadline - now).total_seconds()
        if secondsTotal < 0: # when isExpired
            secondsTotal = secondsTotal * -1
        if secondsTotal >= 24*3600: # 1 day
            secondsOffset = secondsTotal % (24*3600)
            days = int((secondsTotal - secondsOffset) / (24*3600))
            secondsTotal = secondsOffset
        if secondsTotal >= 3600: # 1 hour
            secondsOffset = secondsTotal % 3600
            hours = int((secondsTotal - secondsOffset) / 3600)
            secondsTotal = secondsOffset
        if secondsTotal >= 60:
            secondsOffset = secondsTotal % 60
            mins = int((secondsTotal - secondsOffset) / 60)
        text = 'ago' if self.isExpired() else 'remaining'
        if days < 1 and hours < 1:
            return '{} m {}'.format(mins, text)
        elif days < 1:
            return '{} h, {} m {}'.format(hours, mins, text)
        else:
            return '{} d, {} h, {} m {}'.format(days, hours, mins, text)

    def remainingTimeSeconds(self):
        now = datetime.now(pytz.timezone('UTC'))
        return (self.deadline - now).total_seconds()

    def setIsDone(self):
        if self.is_done:
            self.is_done = False
        else:
            self.is_done = True
        self.save()

class AppUser(AbstractUser):
    taskGroups = models.ManyToManyField(TaskGroup)
    tasks = models.ManyToManyField(Task)
    showDonePreference = models.BooleanField(default=False)
    timezonePreference = models.CharField(_('Timezone'), max_length=32, choices=tuple(zip(pytz.all_timezones, pytz.all_timezones)), default='UTC')
    datetimeFormatPreference  = models.CharField(_('Datetime format'), max_length=12, choices=tuple(zip(settings.DATETIME_FORMAT_PREFERENCES, settings.DATETIME_FORMAT_PREFERENCES)), default='Y-m-d H:i a')
    languagePreference = models.CharField(_('Language'), max_length=32, choices=settings.LANGUAGES, default='en')
    taskOrderPreference = models.CharField(_('Task order'), max_length=20, default='-priority')
    notifications = models.ManyToManyField(Notification)
    pageNotifications = models.BooleanField(default=True)
    messengerId = models.IntegerField(null=True)
    messengerNotifications = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def GetTasks(self):
        if self.showDonePreference == False:
            return self.tasks.filter(is_done=False).order_by(self.taskOrderPreference)
        return self.tasks.all().order_by(self.taskOrderPreference)

    def GetTaskGroups(self):
        return self.taskGroups.filter(id__in=self.GetTasks().values("group")).order_by('orderIndex')

    def SetShowDonePreference(self):
        if self.showDonePreference:
            self.showDonePreference = False
        else:
            self.showDonePreference = True
        self.save()

    def SetTimezonePreference(self, timezone):
        if "etc/gmt" in timezone.lower():
            timezone = timezone.replace(" ", "+")
        if not (timezone==self.timezonePreference) and timezone in pytz.all_timezones:
            self.timezonePreference = timezone
            self.save()

    def SetDatetimeFormatPreference(self, datetime):
        if not (datetime==self.datetimeFormatPreference) and datetime in settings.DATETIME_FORMAT_PREFERENCES:
            self.datetimeFormatPreference = datetime
            self.save()

    def SetLanguagePreference(self, language):
        if not (language==self.languagePreference):
            for l in settings.LANGUAGES:
                if language in l:
                    self.languagePreference = language
                    self.save()
                    break

    def SetTaskOrderPreference(self, order):
        self.taskOrderPreference = order
        self.save()

    def SetPageNotifications(self, value):
        self.pageNotifications = value
        self.save()

    def SetMessengerNotifications(self, value):
        self.messengerNotifications = value
        if value:
            r = MessengerApiHandler().SendResponseMessage(self.messengerId, "Notifications enabled.")
        else:
            r = MessengerApiHandler().SendResponseMessage(self.messengerId, "Notifications disabled.")
        self.save()

    def SetMessengerId(self, value):
        self.messengerId = value
        self.save()

    def NewNotificaton(self, notification):
        if self.pageNotifications:
            self.notifications.add(Notification.objects.create(recipient_user_id=notification.recipient_user_id, details=notification.details, notification_time=notification.notification_time, sent=True))
        if self.messengerNotifications and self.messengerId:
            r = MessengerApiHandler().SendNotificationMessage(self.messengerId, notification.details)

def get_default_token_expirationDate():
    return datetime.now(timezone.utc)+timedelta(minutes=10)

class MessengerToken(models.Model):
    token = models.CharField(max_length=60)
    expirationDate = models.DateTimeField(default=get_default_token_expirationDate)
    messengerId = models.IntegerField()

    def isExpired(self):
        now = datetime.now(timezone.utc)
        return now > self.expirationDate
