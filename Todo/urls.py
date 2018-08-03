from django.contrib import admin
from django.urls import path
from todoapp import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url(r'tcreate/$', views.TaskCreate.as_view(), name='TaskCreate'),
    url(r'tgcreate/$', views.TaskGroupCreate.as_view(), name='TaskGroupCreate'),
    url(r'^(?P<pk>[0-9]+)/tgupdate/$', views.TaskGroupUpdate.as_view(), name='TaskGroupUpdate'),
    url(r'^(?P<pk>[0-9]+)/tupdate/$', views.TaskUpdate.as_view(), name='TaskUpdate'),
    url(r'^(?P<pk>[0-9]+)/tgdelete/$', views.TaskGroupDelete.as_view(), name='TaskGroupDelete'),
    url(r'^(?P<pk>[0-9]+)/tdelete/$', views.TaskDelete.as_view(), name='TaskDelete'),
    url(r'^(?P<task_id>[0-9]+)/IsDoneUpdate/$', views.IsDoneUpdate, name='IsDoneUpdate'),
    path('admin/', admin.site.urls),
]
