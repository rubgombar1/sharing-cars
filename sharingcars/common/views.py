# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.edit import UpdateView
from django.http import HttpResponse

from common.models import User, Message, Folder
from common.forms import UserRegisterForm, UserBaseForm, MessageForm
from routes.models import CommentRoute
from announcements.models import CommentAnnouncement



class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')
    success_message = u"Te has registrado correctamente en la aplicación"

    def get_success_url(self):
        form = self.get_form()
        new_user = authenticate(username=form.data['username'], password=form.data['password'])
        login(self.request, new_user)
        return self.success_url.format()


class UserProfileView(DetailView):
    model = User
    template_name = 'common/user/profile.html'
    context_object_name = 'custom_user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        try:
            obj = User.objects.get(user_account__username=username)
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': User._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['comments_routes'] = CommentRoute.objects.filter(route__user__user_account__username=self.kwargs.get('username', ''))
        context['comments_announcements'] = CommentAnnouncement.objects.filter(announcement__user__user_account__username=self.kwargs.get('username', ''))
        return context


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserBaseForm
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')
    success_message = u"Has actualizado los datos de tu perfil correctamente"
    context_object_name = 'custom_user'

    def get_success_url(self):
        return self.success_url.format()

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        try:
            obj = User.objects.get(user_account__username=username)
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': User._meta.verbose_name})
        return obj


class MessageCreateView(SuccessMessageMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'common/message/create.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url.format()

    def get_initial(self):
        initial = super(MessageCreateView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        instance = form.save(commit=False)
        sender = User.objects.get(user_account__id=self.request.user.id)
        folder = sender.folder_set.get(name="Bandeja de salida")
        instance.sender = sender
        instance.folder = folder
        return super(MessageCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Su mensaje a "%s" se ha enviado correctamente' % cleaned_data.get('recipient').user_account.username


class FolderDetailsView(DetailView):
    model = Message
    template_name = 'common/message/show.html'

    def get_object(self, queryset=None):
        type = self.kwargs.get('type')
        try:
            user = User.objects.get(user_account__pk=self.request.user.id)
            if type == 'income':
                obj = user.folder_set.get(name='Bandeja de entrada')
            elif type == 'outcome':
                obj = user.folder_set.get(name='Bandeja de salida')
            elif type == 'draft':
                obj = user.folder_set.get(name='Papelera')
            else:
                raise Http404(_("No se ha encontrado la bandeja de mensajes que busca"))
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': User._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super(FolderDetailsView, self).get_context_data(**kwargs)
        context['type'] = self.kwargs.get('type')
        return context


class MessageDetailsView(FolderDetailsView):

    def get_context_data(self, **kwargs):
        context = super(MessageDetailsView, self).get_context_data(**kwargs)
        message = self.object.message_set.get(pk=self.kwargs.get('pk', 0))
        message.open = True
        message.save()
        context['message_see'] = message
        return context


def ajax_delete_message(request, pk):
    result = Message.objects.filter(pk=pk)
    if request.is_ajax() and result:
        message = result[0]
        user = User.objects.get(user_account__pk=request.user.pk)
        message.folder =user.folder_set.get(name='Papelera')
        message.save()
        return HttpResponse(reverse_lazy('messages-see', kwargs={'type': 'draft', 'pk': pk}))
    else:
        return HttpResponse('Error')


def ajax_hide_message(request, pk, type):
    result = Message.objects.filter(pk=pk)
    if request.is_ajax() and result:
        message = result[0]
        message.open = False
        message.save()
        return HttpResponse(reverse_lazy('messages-details', kwargs={'type': type }))
    else:
        return HttpResponse('Error')


class ReplyMessageView(MessageCreateView):

    def get_initial(self):
        initial = super(ReplyMessageView, self).get_initial()
        initial['user'] = self.request.user
        initial['sender_id'] = Message.objects.get(pk=self.kwargs.get('pk', 0)).sender.pk
        return initial