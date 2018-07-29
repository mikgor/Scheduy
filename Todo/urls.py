from django.contrib import admin
from django.urls import path
from todoapp import views
from django.conf.urls import url


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/tgupdate/$', views.TaskGroupUpdate.as_view(), name='TaskGroupUpdate'),
    url(r'^(?P<pk>[0-9]+)/tupdate/$', views.TaskUpdate.as_view(), name='TaskUpdate'),
    url(r'^(?P<pk>[0-9]+)/tgdelete/$', views.TaskGroupDelete.as_view(), name='TaskGroupDelete'),
    url(r'^(?P<pk>[0-9]+)/tdelete/$', views.TaskDelete.as_view(), name='TaskDelete'),
    path('admin/', admin.site.urls),
]
