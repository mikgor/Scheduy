from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
import pdb
import pytz
class TaskGroup(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=30, default="whitesmoke")

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=40)
    details = models.CharField(max_length=80, blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField('Deadline')
    priority = models.PositiveSmallIntegerField(default=1)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)

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
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezonePreference = models.CharField('Timezone', max_length=32, choices=TIMEZONES, default='UTC')

    def __str__(self):
        return self.email

    def GetTasks(self):
        if self.showDonePreference == False:
            return self.tasks.filter(is_done=False)
        return self.tasks.all()

    def GetTaskGroups(self):
        return self.taskGroups.filter(id__in=self.GetTasks().values("group"))

    def SetShowDonePreference(self):
        if self.showDonePreference:
            self.showDonePreference = False
        else:
            self.showDonePreference = True
        self.save()

    def SetTimezonePreference(self, timezone):
        if timezone in pytz.all_timezones:
            self.timezonePreference = timezone
            self.save()
