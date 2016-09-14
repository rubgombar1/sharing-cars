# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from datetimewidget.widgets import DateTimeWidget
from announcements.models import Announcement, ApplyAnnouncement, StopAnnouncement, CommentAnnouncement
from common.forms import CommentCreateForm



class AnnouncementCreateForm(forms.ModelForm):

    class Meta:
        model = Announcement
        exclude = ('creationMoment', 'user')

    visibility = forms.BooleanField(widget=forms.CheckboxInput(),
                                    label=_('Visible'), required=False)
    origin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-lg-6',
                                                           'placeholder': _('Origen')}),
                             max_length=256, label=_('Origen'), required=True)
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-lg-6',
                                                                'placeholder': _('Destino')}),
                                  max_length=256, label=_('Destino'), required=True)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control col-lg-6'}),
                             label=_('Tipo'), required=True, choices=Announcement.KINDS)
    seating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control col-lg-6',
                                                                 'placeholder': _('Plazas'),
                                                                 'min': '0'}),
                                 validators=[MinValueValidator(0)], label=_('Plazas'))
    unitPrice = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control col-lg-6',
                                                                   'placeholder': _('Precio por plaza'),
                                                                   'min': '0'}),
                                   max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0)], label=_('Precio por plaza'))
    date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3), label=_('Fecha'))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-lg-12',
                                                               'placeholder': _(u'Descripción')}),
                                  label=_(u'Descripción'), required=True)


class ApplyAnnouncementCreateForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba lo que quiera comunicarle al dueño del anuncio.'}), label="Comentario", required=True)

    class Meta:
        model = ApplyAnnouncement
        fields = ('comment', )


class StopAnnouncementForm(forms.ModelForm):
    class Meta:
        model = StopAnnouncement
        exclude = ('announcement', )

    stop = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': _('Parada')}),
                             max_length=256, label=_('Parada'), required=True)

    sequence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control col-lg-6',
                                                                 'placeholder': _('Orden'),
                                                                 'min': '0'}),
                                 validators=[MinValueValidator(0)], label=_('Orden'))


class CommentAnnouncementCreateForm(CommentCreateForm):

    class Meta:
        model = CommentAnnouncement
        exclude = ('user', 'route')
        fields = ['subject', 'rating', 'comment']