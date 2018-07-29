from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, TaskGroup

class IndexView(generic.ListView):
    template_name = 'todoapp/index.html'
    context_object_name = 'taskgroup_list'

    def get_queryset(self):
        return TaskGroup.objects.all()

class TaskGroupUpdate(generic.UpdateView):
    model = TaskGroup
    fields = ['name', 'colour']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')

class TaskUpdate(generic.UpdateView):
    model = Task
    fields = ['name', 'details', 'priority', 'deadline', 'is_done', 'priority']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')

class TaskGroupDelete(DeleteView):
    model = TaskGroup
    success_url = reverse_lazy('index')

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('index')
