# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from datetimewidget.widgets import DateTimeWidget
from announcements.models import Announcement, ApplyAnnouncement



class AnnouncementCreateForm(forms.ModelForm):

    class Meta:
        model = Announcement
        exclude = ('creationMoment', 'user')

    visibility = forms.BooleanField(widget=forms.CheckboxInput(),
                                    label=_('Visible'), required=False)
    origin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-lg-6',
                                                           'placeholder': _('Origin')}),
                             max_length=256, label=_('Origin'), required=True)
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-lg-6',
                                                                'placeholder': _('Destination')}),
                                  max_length=256, label=_('Destination'), required=True)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control col-lg-6'}),
                             label=_('Kind'), required=True, choices=Announcement.KINDS)
    seating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control col-lg-6',
                                                                 'placeholder': _('Number of seats'),
                                                                 'min': '0'}),
                                 validators=[MinValueValidator(0)], label=_('Seats'))
    unitPrice = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control col-lg-6',
                                                                   'placeholder': _('Price for seat'),
                                                                   'min': '0'}),
                                   max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0)], label=_('Price'))
    date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-lg-12',
                                                               'placeholder': _('Description')}),
                                  label=_('Description'), required=True)


class ApplyAnnouncementCreateForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba lo que quiera comunicarle al dueño del anuncio.'}), label="Comentario", required=True)

    class Meta:
        model = ApplyAnnouncement
        fields = ('comment', )