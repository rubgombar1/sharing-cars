# -*- coding: utf-8 -*-
from datetime import date
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User as DjangoUser
from common.models import User, Folder, Message, Actor
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=_("The phone numver must be in this format: "
                                       "'+999999999'. Until 15 characters permited."))


class UserBaseForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': _('Name')}),
                           max_length=64, label=_('Name'))
    surnames = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('Surnames')}),
                               max_length=128, label=_('Surnames'))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': _('City')}),
                           max_length=128, label=_('City'))
    birthdate = forms.DateField(label=_('Birthdate'),
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': date.today()}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '+034 999999999'}),
                            validators=[phone_regex], label=_('Phone number'),
                            max_length=64)


    class Meta:
        model = User
        exclude = ('user_account', )




class UserRegisterForm(UserBaseForm):
    class Meta:
        model = User
        exclude = ('user_account',)

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('User name')}),
                               max_length=32, label=_('User name'))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('Password'),
                                                             'type': 'password'}),
                               max_length=32, label=_('Password'))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'placeholder': _('Confirm Password'),
                                                                     'type': 'password'}),
                                       max_length=32, label=_('Confirm Password'))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Email'}),
                             label=_('Email'), required=True)
    photo = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file'}),
                             label=_('Image'), required=False)


    def save(self, commit=True):
        user_account = DjangoUser.objects.create_user(username=self.data['username'],
                                                      email=self.data['email'],
                                                      password=self.data['password'])
        self.instance.user_account = user_account
        instance = super(UserBaseForm, self).save(commit)
        if commit:
            Folder.objects.get_or_create(name=_('Bandeja de entrada'), actor=instance)
            Folder.objects.get_or_create(name=_('Bandeja de salida'), actor=instance)
            Folder.objects.get_or_create(name=_('Papelera'), actor=instance)

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            self.add_error('password', "Las contraseñas no coinciden.")
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        if DjangoUser.objects.filter(username = self.cleaned_data['username']).exists():
            self.add_error('username', "Ya existe ese nombre de usuario")

        if DjangoUser.objects.filter(email = self.cleaned_data['email']).exists():
            self.add_error('email', "Ya existe un usuario con ese email")


class MessageForm(forms.ModelForm):

    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': _('Asunto')}),
                           max_length=128, label=_('Asunto'), required=True)
    recipient = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select-2'}),
                                  label=_('Receptor'), required=True, queryset=Actor.objects.none())
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': _('Mensaje')}),
                                  label=_('Mensaje'), required=True)



    class Meta:
        model = Message
        exclude = ('folder', 'creationMoment', 'sender')
        fields = ['subject', 'recipient', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        user = kwargs['initial'].pop('user')
        self.fields['recipient'].queryset = Actor.objects.all().exclude(user_account__pk=user.pk)
        self.fields['recipient'].choices = ((x.pk, x.user_account.username) for x in Actor.objects.all().exclude(user_account__pk=user.pk))

    def save(self, commit=True):
        instance = super(MessageForm, self).save(commit)
        if commit:
            clone_message = instance
            clone_message.pk = None
            folder = instance.recipient.folder_set.get(name="Bandeja de entrada")
            clone_message.folder = folder
            clone_message.save()
        return instance