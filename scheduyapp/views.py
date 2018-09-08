from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Task, TaskGroup
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.ListView):
    template_name = 'scheduyapp/index.html'
    context_object_name = 'IndexList'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['task_list'] = self.request.user.GetTasks()
            context['taskgroup_list'] = self.request.user.GetTaskGroups()
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskCreateUpdateForm
    template_name = 'scheduyapp/task_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.request.user.tasks.add(self.object)
        self.object.save()
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
        self.object = form.save()
        self.request.user.taskGroups.add(self.object)
        self.object.save()
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
    if showdone is not None:
        request.user.SetShowDonePreference()
    return HttpResponseRedirect(reverse('index'))

class SignUp(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
