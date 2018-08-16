from django.contrib import admin
from django.urls import path
from scheduyapp import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url(r'tcreate/$', views.TaskCreate.as_view(), name='TaskCreate'),
    url(r'tgcreate/$', views.TaskGroupCreate.as_view(), name='TaskGroupCreate'),
    url(r'^(?P<pk>[0-9]+)/tgupdate/$', views.TaskGroupUpdate.as_view(), name='TaskGroupUpdate'),
    url(r'^(?P<pk>[0-9]+)/tupdate/$', views.TaskUpdate.as_view(), name='TaskUpdate'),
    url(r'^(?P<pk>[0-9]+)/tgdelete/$', views.TaskGroupDelete.as_view(), name='TaskGroupDelete'),
    url(r'^(?P<pk>[0-9]+)/tdelete/$', views.TaskDelete.as_view(), name='TaskDelete'),
    url(r'^(?P<task_id>[0-9]+)/IsDoneUpdate/$', views.IsDoneUpdate, name='IsDoneUpdate'),
    url(r'^setpreference/$', views.SetUserPreference, name='SetUserPreference'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
