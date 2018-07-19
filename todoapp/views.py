from django.views import generic
from .models import Task

class IndexView(generic.ListView):
    template_name = 'todoapp/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.all()
