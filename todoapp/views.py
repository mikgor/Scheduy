from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, TaskGroup
from .forms import *

class IndexView(generic.ListView):
    template_name = 'todoapp/index.html'
    context_object_name = 'IndexList'
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['task_list'] = Task.objects.all()
        context['taskgroup_list'] = TaskGroup.objects.all()
        return context

class TaskCreate(CreateView):
    form_class = TaskCreateUpdateForm
    template_name = 'todoapp/task_form.html'
    success_url = reverse_lazy('index')

class TaskGroupCreate(CreateView):
    form_class = TaskGroupCreateUpdateForm
    template_name = 'todoapp/taskgroup_form.html'
    success_url = reverse_lazy('index')

class TaskGroupUpdate(UpdateView):
    model = TaskGroup
    form_class = TaskGroupCreateUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskCreateUpdateForm
    template_name = 'todoapp/task_update_form.html'
    success_url = reverse_lazy('index')

class TaskGroupDelete(DeleteView):
    model = TaskGroup
    success_url = reverse_lazy('index')

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('index')
