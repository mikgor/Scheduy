from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser

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
        now = datetime.now(timezone.utc)
        seconds = (self.deadline - now).total_seconds()
        hours = seconds / 3600
        days = hours / 24
        mins = hours * 60
        if self.isExpired():
            if -days < 1 and -hours < 1:
                return '{} m ago.'.format(round(-mins))
            elif -days < 1:
                return '{} h, {} m ago'.format(round(-hours), round(-mins%60))
            else:
                return '{} d, {} h, {} m ago'.format(round(-days), round(-hours%24), round(-mins%60))
        else:
            if days < 1 and hours < 1:
                return '{} m remaining.'.format(round(mins))
            elif days < 1:
                return '{} h, {} m remaining'.format(round(hours), round(mins%60))
            else:
                return '{} d, {} h, {} m remaining'.format(round(days), round(hours%24), round(mins%60))

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

    def __str__(self):
        return self.email

    def SetShowDonePreference(self):
        if self.showDonePreference:
            self.showDonePreference = False
        else:
            self.showDonePreference = True
        self.save()
