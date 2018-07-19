from django.contrib import admin
from django.urls import path
from todoapp import views
from django.conf.urls import url


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/tgupdate/$', views.TaskGroupUpdate.as_view(), name='TaskGroupUpdate'),
    path('admin/', admin.site.urls),
]
