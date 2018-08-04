from django import forms
from .models import Task, TaskGroup

class TaskCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'details', 'priority', 'deadline', 'priority', 'group')
        widgets = {'deadline': forms.HiddenInput()}

class TaskGroupCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = TaskGroup
        fields = ('name', 'color')
        widgets = {'color': forms.HiddenInput()}
