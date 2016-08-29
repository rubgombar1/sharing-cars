# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView

from common.models import User
from common.forms import UserRegisterForm


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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        return context