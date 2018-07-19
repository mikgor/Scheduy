from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField('Deadline')
    priority = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

class TaskGroup(models.Model):
    name = models.CharField(max_length=200)
    colour = models.CharField(max_length=30, default="whitesmoke")
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name
