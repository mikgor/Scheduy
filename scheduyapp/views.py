from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Task, TaskGroup
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
import pytz
from django.utils import timezone
from datetime import timezone, datetime
from django.utils import translation
from django.conf import settings

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'scheduyapp/index.html'
    context_object_name = 'IndexList'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.user.languagePreference
            context['task_list'] = self.request.user.GetTasks()
            context['taskgroup_list'] = self.request.user.GetTaskGroups()
            context['total_task_count'] = self.request.user.tasks.all().count()
            context['total_taskgroup_count'] = self.request.user.taskGroups.all().count()
            context['groups_limit'] = settings.GROUPS_LIMIT_PERUSER
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskCreateUpdateForm
    template_name = 'scheduyapp/task_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        convertedToPreferenced = pytz.timezone(self.request.user.timezonePreference).localize(self.object.deadline.replace(tzinfo=None))
        self.object.deadline = convertedToPreferenced.astimezone(pytz.timezone('UCT'))
        self.object.save()
        self.request.user.tasks.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class TaskGroupCreate(LoginRequiredMixin, CreateView):
    form_class = TaskGroupCreateUpdateForm
    template_name = 'scheduyapp/taskgroup_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if self.request.user.taskGroups.count() >= settings.GROUPS_LIMIT_PERUSER:
            return HttpResponseRedirect(reverse('index'))
        self.object = form.save()
        self.object.initializeOrderIndex(self.request.user.taskGroups.all().order_by('orderIndex').last())
        self.request.user.taskGroups.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

class TaskGroupUpdate(LoginRequiredMixin, UpdateView):
    model = TaskGroup
    form_class = TaskGroupCreateUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        group = ''
        try:
            group = self.request.user.taskGroups.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('index'))
        return super(TaskGroupUpdate, self).get(request, *args, **kwargs)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateUpdateForm
    template_name = 'scheduyapp/task_update_form.html'
    success_url = reverse_lazy('index')

    def get_initial(self):
        initial = super(TaskUpdate, self).get_initial()
        task = self.get_object()
        initial['deadline'] = task.deadline.astimezone(pytz.timezone(self.request.user.timezonePreference)).replace(tzinfo=pytz.timezone('UTC'))
        return initial

    def get(self, request, *args, **kwargs):
        task = ''
        try:
            task = self.request.user.tasks.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('index'))
        return super(TaskUpdate, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        convertedToPreferenced = pytz.timezone(self.request.user.timezonePreference).localize(self.object.deadline.replace(tzinfo=None))
        self.object.deadline = convertedToPreferenced.astimezone(pytz.timezone('UCT'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class TaskGroupDelete(LoginRequiredMixin, DeleteView):
    model = TaskGroup
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        group = ''
        try:
            group = self.request.user.taskGroups.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('index'))
        return super(TaskGroupDelete, self).get(request, *args, **kwargs)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        task = ''
        try:
            task = self.request.user.tasks.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('index'))
        return super(TaskDelete, self).get(request, *args, **kwargs)

def IsDoneUpdate(request, task_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    task = ''
    try:
        task = request.user.tasks.get(pk=task_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    task.setIsDone()
    return HttpResponseRedirect(reverse('index'))

def SetUserPreference(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    showdone = request.GET.get('showdone', None)
    timezone = request.GET.get('timezone', None)
    datetimeFormatPreference = request.GET.get('datetimeFormatPreference', None)
    language = request.GET.get('language', None)
    order = request.GET.get('taskorder', None)
    moveup = request.GET.get('moveup', None)
    if showdone is not None:
        request.user.SetShowDonePreference()
    if timezone is not None:
        request.user.SetTimezonePreference(timezone)
    if datetimeFormatPreference is not None:
        request.user.SetDatetimeFormatPreference(datetimeFormatPreference)
    if language is not None:
        request.user.SetLanguagePreference(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = request.user.languagePreference
    if order is not None:
        request.user.SetTaskOrderPreference(order)
    if moveup is not None:
        userGroups = request.user.GetTaskGroups()
        userGroups.get(id=moveup).setOrderIndex(userGroups)
    return HttpResponseRedirect(reverse('index'))

class SignUp(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def UserUpdate(request):
    context = {}
    context['timezone_list'] = pytz.all_timezones
    context['language_list'] = tuple(settings.LANGUAGES)
    context['datetimeformat_list'] = settings.DATETIME_FORMAT_PREFERENCES
    context['datetimeNow'] = pytz.timezone(request.user.timezonePreference).localize(datetime.now().replace(tzinfo=None)).astimezone(pytz.timezone('UCT'))

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    return render(request, 'registration/userupdate.html', context)
