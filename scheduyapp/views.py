from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Task, TaskGroup, Notification, MessengerToken
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
import pytz
from django.utils import timezone
from datetime import timezone, datetime
from django.utils import translation
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from Scheduy.local_settings import *
from django.views.decorators.csrf import csrf_exempt
from .classes.messengerApiHandler import MessengerApiHandler
import json
import secrets

def IndexView(request):
    return render(request, 'scheduy/index.html')

class DashboardView(LoginRequiredMixin, generic.ListView):
    template_name = 'scheduyapp/dashboard.html'
    context_object_name = 'dashboardList'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.user.languagePreference
            context['task_list'] = self.request.user.GetTasks()
            context['taskgroup_list'] = self.request.user.GetTaskGroups()
            context['notification_list'] = self.request.user.notifications.all()
            context['total_task_count'] = self.request.user.tasks.all().count()
            context['total_taskgroup_count'] = self.request.user.taskGroups.all().count()
            context['total_notification_count'] = self.request.user.notifications.all().count()
            context['groups_limit'] = settings.GROUPS_LIMIT_PERUSER
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskCreateUpdateForm
    template_name = 'scheduyapp/task_form.html'
    success_url = reverse_lazy('dashboard')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        convertedToPreferencedDeadline = ''
        if self.object.deadline:
            convertedToPreferencedDeadline = pytz.timezone(self.request.user.timezonePreference).localize(self.object.deadline.replace(tzinfo=None))
            self.object.deadline = convertedToPreferencedDeadline.astimezone(pytz.timezone('UCT'))
        if self.object.notification_time:
            convertedToPreferencedNotification = pytz.timezone(self.request.user.timezonePreference).localize(self.object.notification_time.replace(tzinfo=None))
            notificationTime = convertedToPreferencedNotification.astimezone(pytz.timezone('UCT'))
            if datetime.now(timezone.utc) < notificationTime:
                detailsText = self.object.name
                if convertedToPreferencedDeadline:
                     detailsText += " " + convertedToPreferencedDeadline.strftime(self.request.user.datetimeFormatPreference.replace('H:i a', '%I:%M').replace('m', '%m').replace('d', '%d').replace('Y', '%Y').replace('H', '%H').replace('i', '%M'))
                notification = Notification.objects.create(recipient_user_id=self.request.user.id, details=detailsText, notification_time=notificationTime)
                self.object.notification = notification
                self.object.notification_time = notificationTime
            else:
                form.add_error('', _('Notification time field must be later than now'))
                return self.form_invalid(form)
        self.object.save()
        self.request.user.tasks.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class TaskGroupCreate(LoginRequiredMixin, CreateView):
    form_class = TaskGroupCreateUpdateForm
    template_name = 'scheduyapp/taskgroup_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        if self.request.user.taskGroups.count() >= settings.GROUPS_LIMIT_PERUSER:
            return HttpResponseRedirect(reverse('dashboard'))
        self.object = form.save()
        self.object.initializeOrderIndex(self.request.user.taskGroups.all().order_by('orderIndex').last())
        self.request.user.taskGroups.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

class TaskGroupUpdate(LoginRequiredMixin, UpdateView):
    model = TaskGroup
    form_class = TaskGroupCreateUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        group = ''
        try:
            group = self.request.user.taskGroups.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('dashboard'))
        return super(TaskGroupUpdate, self).get(request, *args, **kwargs)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateUpdateForm
    template_name = 'scheduyapp/task_update_form.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super(TaskUpdate, self).get_initial()
        task = self.get_object()
        if task.deadline:
            initial['deadline'] = task.deadline.astimezone(pytz.timezone(self.request.user.timezonePreference)).replace(tzinfo=pytz.timezone('UTC'))
        if task.notification_time:
            initial['notification_time'] = task.notification_time.astimezone(pytz.timezone(self.request.user.timezonePreference)).replace(tzinfo=pytz.timezone('UTC'))
        return initial

    def get(self, request, *args, **kwargs):
        task = ''
        try:
            task = self.request.user.tasks.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('dashboard'))
        return super(TaskUpdate, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        convertedToPreferencedDeadline = ""
        if self.object.deadline:
            convertedToPreferencedDeadline = pytz.timezone(self.request.user.timezonePreference).localize(self.object.deadline.replace(tzinfo=None))
            self.object.deadline = convertedToPreferencedDeadline.astimezone(pytz.timezone('UCT'))
        if self.object.notification_time:
            convertedToPreferencedNotification = pytz.timezone(self.request.user.timezonePreference).localize(self.object.notification_time.replace(tzinfo=None))
            notificationTime = convertedToPreferencedNotification.astimezone(pytz.timezone('UCT'))
            if datetime.now(timezone.utc) < notificationTime:
                detailsText = self.object.name
                if convertedToPreferencedDeadline:
                    detailsText+ " " + convertedToPreferencedNotification.strftime(self.request.user.datetimeFormatPreference.replace('H:i a', '%I:%M').replace('m', '%m').replace('d', '%d').replace('Y', '%Y').replace('H', '%H').replace('i', '%M'))
                notification = None
                if self.object.notification:
                    notification = Notification.objects.all().filter(id=self.object.notification.id).first()
                    notification.details = detailsText
                    notification.notification_time = notificationTime
                else:
                    notification = Notification.objects.create(recipient_user_id=self.request.user.id, details=detailsText, notification_time=notificationTime)
                notification.save()
                self.object.notification_time = notificationTime
                self.object.notification = notification
            else:
                form.add_error('', _('Notification time field must be later than now'))
                return self.form_invalid(form)
        else:
            if self.object.notification:
                if self.request.user.GetTasks().filter(notification_id=self.object.notification.id).exists():
                    Notification.objects.filter(id=self.object.notification.id).delete()
                    self.object.notification = None
                    self.object.notification_time = None
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class TaskGroupDelete(LoginRequiredMixin, DeleteView):
    model = TaskGroup
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        group = ''
        try:
            group = self.request.user.taskGroups.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('dashboard'))
        return super(TaskGroupDelete, self).get(request, *args, **kwargs)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        task = ''
        try:
            task = self.request.user.tasks.get(pk=self.get_object().id)
        except:
            return HttpResponseRedirect(reverse('dashboard'))
        return super(TaskDelete, self).get(request, *args, **kwargs)

def IsDoneUpdate(request, task_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    task = ''
    try:
        task = request.user.tasks.get(pk=task_id)
    except:
        return HttpResponseRedirect(reverse('dashboard'))
    task.setIsDone()
    return HttpResponseRedirect(reverse('dashboard'))

def SetUserPreference(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    showdone = request.GET.get('showdone', None)
    timezone = request.GET.get('timezone', None)
    datetimeFormatPreference = request.GET.get('datetimeFormatPreference', None)
    language = request.GET.get('language', None)
    order = request.GET.get('taskorder', None)
    moveup = request.GET.get('moveup', None)
    pageNotifications = request.GET.get('pageNotifications', None)
    messengerNotifications = request.GET.get('messengerNotifications', None)
    if showdone is not None:
        request.user.SetShowDonePreference()
    if timezone is not None:
        request.user.SetTimezonePreference(timezone)
    if datetimeFormatPreference is not None:
        request.user.SetDatetimeFormatPreference(datetimeFormatPreference)
    if language is not None:
        request.user.SetLanguagePreference(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = request.user.languagePreference
    if order is not None:
        request.user.SetTaskOrderPreference(order)
    if moveup is not None:
        userGroups = request.user.GetTaskGroups()
        userGroups.get(id=moveup).setOrderIndex(userGroups)
    if pageNotifications:
        request.user.SetPageNotifications(True if pageNotifications == "true" else False)
    if messengerNotifications:
        if messengerNotifications == "false":
            request.user.SetMessengerNotifications(False)
    return HttpResponseRedirect(reverse('dashboard'))

class SignUp(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def UserUpdate(request):
    context = {}
    context['timezone_list'] = pytz.all_timezones
    context['language_list'] = tuple(settings.LANGUAGES)
    context['datetimeformat_list'] = settings.DATETIME_FORMAT_PREFERENCES
    context['datetimeNow'] = pytz.timezone(request.user.timezonePreference).localize(datetime.now().replace(tzinfo=None)).astimezone(pytz.timezone('UCT'))

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    return render(request, 'registration/userupdate.html', context)

def NotificationRead(request, notification_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    notification = ''
    try:
        notification = request.user.notifications.get(pk=notification_id)
    except:
        return HttpResponseRedirect(reverse('dashboard'))
    request.user.notifications.remove(notification)
    return HttpResponseRedirect(reverse('dashboard'))

def SendNotifications(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")

    for notification in Notification.objects.filter(sent=False):
        if notification.timeLeft():
            notification.Send()
            Notification.objects.get(pk=notification.id).delete()
    return HttpResponse("OK")

@csrf_exempt
def MessengerRequest(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")
    data = json.loads(request.body.decode("utf-8"))
    messaging = data['entry'][0]['messaging'][0]
    print(data)
    messengerId = messaging['sender']['id']
    messageAttachments = ''
    messageAttachmentsType = ''
    postbackPayload = ''
    quickReplyPayload = ''
    if 'message' in messaging:
        if 'text' in messaging['message']:
            messageAttachments = 'text'
            if 'quick_reply' in messaging['message']:
                quickReplyPayload = "<POSTBACK_PAYLOAD>"
        else:
            messageAttachments = messaging['message']['attachments'][0]
            messageAttachmentsType = messaging['message']['attachments'][0]['type']
    if not messageAttachments:
        postbackPayload = messaging['postback']['payload']
    if quickReplyPayload == "<POSTBACK_PAYLOAD>":
        user = AppUser.objects.get(messengerId=messengerId)
        payloadText = messaging['message']['quick_reply']['payload']
        if payloadText == "<ENABLE_PAYLOAD>":
            enabled = False
            if user:
                if user.messengerNotifications:
                    enabled = True
                    r = MessengerApiHandler().SendResponseMessage(messengerId, "You have notifications enabled already.")
            if not enabled:
                token = ''
                if MessengerToken.objects.filter(messengerId=messengerId).exists():
                    token = MessengerToken.objects.get(messengerId=messengerId).token
                else:
                    mToken = MessengerToken.objects.create(messengerId=messengerId, token=secrets.token_hex(25))
                    token = mToken.token
                r = MessengerApiHandler().SendConnectMessage(messengerId, token)
        if payloadText == "<DISABLE_PAYLOAD>":
            disabled = False
            if user:
                if user.messengerNotifications:
                    disabled = True
                    user.SetMessengerNotifications(False)
            if not disabled:
                r = MessengerApiHandler().SendResponseMessage(messengerId, "You don't have notifications enabled yet.")
        if payloadText == "<HELP_PAYLOAD>":
            r = MessengerApiHandler().SendAutoResponseMessage(messengerId, 'help')
    elif postbackPayload and postbackPayload == "GET_STARTED_PAYLOAD":
        r = MessengerApiHandler().SendResponseMessage(messengerId, "Welcome. If you want to enable Messenger notifications click 'Enable notifications' below. You can disable notifications at any time using 'Disable notifications'.")
    else:
        text = ''
        if messageAttachments == 'text':
            text = messaging['message']['text']
        r = MessengerApiHandler().SendAutoResponseMessage(messengerId, text.lower())
    return HttpResponse("OK")

def ConnectMessenger(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    token = request.GET.get('token', None)
    if token and MessengerToken.objects.filter(token=token).exists():
        mToken = MessengerToken.objects.get(token=token)
        request.user.SetMessengerId(mToken.messengerId)
        request.user.SetMessengerNotifications(True)
        mToken.delete()
    else:
        return render(request, "scheduyapp/error_page.html", {'error': _("Authorization token has expired. You can generate new one using Enable notifictions button.")})
    return HttpResponseRedirect(reverse('UserUpdate'))

def ExpireMessengerTokens(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")
    for token in MessengerToken.objects.all():
        if token.isExpired():
            token.delete()
    return HttpResponse("OK")

def HelpMessengerConnection(request):
    return render(request, "scheduyapp/help_messengerconnection.html")
