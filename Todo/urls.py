from django.contrib import admin
from django.urls import path
from todoapp import views

app_name = 'todoapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]
