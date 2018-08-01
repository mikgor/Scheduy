from django.db import models

class TaskGroup(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=30, default="whitesmoke")

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField('Deadline')
    priority = models.PositiveSmallIntegerField(default=1)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
