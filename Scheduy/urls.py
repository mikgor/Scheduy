from django.contrib import admin
from django.urls import path
from scheduyapp import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.IndexView, name='index'),
    url('^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'tcreate/$', views.TaskCreate.as_view(), name='TaskCreate'),
    url(r'tgcreate/$', views.TaskGroupCreate.as_view(), name='TaskGroupCreate'),
    url(r'^(?P<pk>[0-9]+)/tgupdate/$', views.TaskGroupUpdate.as_view(), name='TaskGroupUpdate'),
    url(r'^(?P<pk>[0-9]+)/tupdate/$', views.TaskUpdate.as_view(), name='TaskUpdate'),
    url(r'^(?P<pk>[0-9]+)/tgdelete/$', views.TaskGroupDelete.as_view(), name='TaskGroupDelete'),
    url(r'^(?P<pk>[0-9]+)/tdelete/$', views.TaskDelete.as_view(), name='TaskDelete'),
    url(r'^(?P<task_id>[0-9]+)/IsDoneUpdate/$', views.IsDoneUpdate, name='IsDoneUpdate'),
    url(r'^(?P<notification_id>[0-9]+)/NotificationRead/$', views.NotificationRead, name='NotificationRead'),
    url(r'^setpreference/$', views.SetUserPreference, name='SetUserPreference'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^userupdate/$', views.UserUpdate, name='UserUpdate'),
    url(r'^sendnotifications/$', views.SendNotifications, name='SendNotifications'),
    url(r'^messengerrequest/$', views.MessengerRequest, name='MessengerRequest'),
    url(r'^connectmessenger/$', views.ConnectMessenger, name='connectmessenger'),
    url(r'^confirmemail/$', views.ConfirmEmail, name='ConfirmEmail'),
    url(r'^expiremessengertokens/$', views.ExpireMessengerTokens, name='ExpireMessengerTokens'),
    url(r'^expireemailtokens/$', views.ExpireEmailTokens, name='ExpireEmailTokens'),
    url(r'^help_messengerconnection/$', views.HelpMessengerConnection, name='HelpMessengerConnection'),
    url(r'^mailing/$', views.MailingService, name='mailing'),
    url(r'^accountcreated/$', views.AccountCreated, name='AccountCreated'),
    url(r'^resendemailtoken/$', views.ResendEmailToken, name='ResendEmailToken'),
    path('admin/', admin.site.urls),
]
