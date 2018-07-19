from django.views import generic
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Task, TaskGroup

class IndexView(generic.ListView):
    template_name = 'todoapp/index.html'
    context_object_name = 'taskgroup_list'

    def get_queryset(self):
        return TaskGroup.objects.all()

class TaskGroupUpdate(generic.UpdateView):
    model = TaskGroup
    fields = ['name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')
