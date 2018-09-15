from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Task, TaskGroup, AppUser

class TaskCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'details', 'priority', 'deadline', 'priority', 'group')
        widgets = {'deadline': forms.HiddenInput()}

    def __init__(self, user, *args, **kwargs):
        super(TaskCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = user.taskGroups.all()

class TaskGroupCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = TaskGroup
        fields = ('name', 'color')
        widgets = {'color': forms.HiddenInput()}

class AppUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username', 'email', 'timezonePreference')

class AppUserChangeForm(forms.ModelForm):

    class Meta:
        model = AppUser
        fields = ('timezonePreference',)
        exclude = ('password',)
