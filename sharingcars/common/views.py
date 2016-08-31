# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.edit import UpdateView

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
        context['comments_routes'] = CommentRoute.objects.filter(route__user__user_account__pk=self.request.user.pk)
        context['comments_announcements'] = CommentAnnouncement.objects.filter(announcement__user__user_account__pk=self.request.user.pk)
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
    model = User
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


class MessageDetailsView(DetailView):
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
                raise Http404(_("No se ha encontrado la bandeja de mensajes"))
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': User._meta.verbose_name})
        return obj