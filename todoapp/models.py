from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField('Deadline')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
