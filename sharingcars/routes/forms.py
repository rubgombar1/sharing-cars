# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from routes.models import Route


class RouteCreateForm(forms.ModelForm):
    class Meta:
        model = Route
        exclude = ('visibility', 'creationMoment', 'user')

    origin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': _('Origin')}),
                             max_length=64, label=_('Origin'), required=True)
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': _('Destination')}),
                                  max_length=64, label=_('Destination'), required=True)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label=_('Kind'), required=True, choices=Route.KINDS)
    seating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                 'placeholder': _('Number of seats'),
                                                                 'min': '0'}),
                                 validators=[MinValueValidator(0)], label=_('Seats'))
    unitPrice = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                   'placeholder': _('Price for seat'),
                                                                   'min': '0'}),
                                   max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0)], label=_('Price'))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'placeholder': _('Description')}),
                                  label=_('Description'), required=True)

    # Monday
    monday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Depart time')}),
                                        max_length=32, label=_('Depart time'), required=False)
    monday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Return time')}),
                                        max_length=32, label=_('Return time'), required=False)
    # Tuesday
    tuesday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': _('Depart time')}),
                                         max_length=32, label=_('Depart time'), required=False)
    tuesday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': _('Return time')}),
                                         max_length=32, label=_('Return time'), required=False)
    # Wednesday
    wednesday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': _('Depart time')}),
                                           max_length=32, label=_('Depart time'), required=False)
    wednesday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': _('Return time')}),
                                           max_length=32, label=_('Return time'), required=False)
    # Thursday
    thursday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': _('Depart time')}),
                                          max_length=32, label=_('Depart time'), required=False)
    thursday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': _('Return time')}),
                                          max_length=32, label=_('Return time'), required=False)
    # Friday
    friday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Depart time')}),
                                        max_length=32, label=_('Depart time'), required=False)
    friday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Return time')}),
                                        max_length=32, label=_('Return time'), required=False)
    # Saturday
    saturday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': _('Depart time')}),
                                          max_length=32, label=_('Depart time'), required=False)
    saturday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': _('Return time')}),
                                          max_length=32, label=_('Return time'), required=False)
    # Sunday
    sunday_departTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Depart time')}),
                                        max_length=32, label=_('Depart time'), required=False)
    sunday_returnTime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': _('Return time')}),
                                        max_length=32, label=_('Return time'), required=False)

    def clean(self):
        monday_departTime = self.cleaned_data['monday_departTime']
        monday_returnTime = self.cleaned_data['monday_returnTime']

        tuesday_departTime = self.cleaned_data['tuesday_departTime']
        tuesday_returnTime = self.cleaned_data['tuesday_returnTime']

        wednesday_departTime = self.cleaned_data['wednesday_departTime']
        wednesday_returnTime = self.cleaned_data['wednesday_returnTime']

        thursday_departTime = self.cleaned_data['thursday_departTime']
        thursday_returnTime = self.cleaned_data['thursday_returnTime']

        friday_departTime = self.cleaned_data['friday_departTime']
        friday_returnTime = self.cleaned_data['friday_returnTime']

        saturday_departTime = self.cleaned_data['saturday_departTime']
        saturday_returnTime = self.cleaned_data['saturday_returnTime']

        sunday_departTime = self.cleaned_data['sunday_departTime']
        sunday_returnTime = self.cleaned_data['sunday_returnTime']

        # Validations for departTime and returnTime of Monday
        if (monday_returnTime == "" and monday_departTime !="") or (monday_returnTime != "" and monday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el lunes no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(monday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el lunes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(monday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el lunes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(monday_departTime, monday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el lunes debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Tuesday
        if (tuesday_returnTime == "" and tuesday_departTime !="") or (tuesday_returnTime != "" and tuesday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el martes no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(tuesday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el martes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(tuesday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el martes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(tuesday_departTime, tuesday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el martes debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Wednesday
        if (wednesday_returnTime == "" and wednesday_departTime !="") or (wednesday_returnTime != "" and wednesday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el miércoles no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(wednesday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el miércoles no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(wednesday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el miércoles no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(wednesday_departTime, wednesday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el miércoles debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Thursday
        if (thursday_returnTime == "" and thursday_departTime !="") or (thursday_returnTime != "" and thursday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el jueves no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(thursday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el jueves no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(thursday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el jueves no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(thursday_departTime, thursday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el jueves debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Friday
        if (friday_returnTime == "" and friday_departTime !="") or (friday_returnTime != "" and friday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el viernes no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(friday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el viernes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(friday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el viernes no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(friday_departTime, friday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el viernes debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Saturday
        if (saturday_returnTime == "" and saturday_departTime !="") or (saturday_returnTime != "" and saturday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el sábado no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(saturday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el sábado no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(saturday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el sábado no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(saturday_departTime, saturday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el sábado debe de ser posterior a la hora de salida")

        # Validations for departTime and returnTime of Sunday
        if (sunday_returnTime == "" and sunday_departTime !="") or (sunday_returnTime != "" and sunday_departTime ==""):
            self.add_error('monday_departTime', "La hora de salida y de vuelta para el domingo no están bien configuradas, por favor, corríjalo y vuelva a enviar")
        else:
            if validate_hour(sunday_departTime):
                self.add_error('monday_departTime', "La hora de salida para el domingo no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif  validate_hour(sunday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el domingo no tiene la estructura correcta (Por ejemplo: 15:30)")
            elif validate_depart_return(sunday_departTime, sunday_returnTime):
                self.add_error('monday_departTime', "La hora de vuelta para el domingo debe de ser posterior a la hora de salida")


# Validate that a hour is between 00:00 and 23:59.
def validate_hour(hour):
    error = False
    if hour != "":
        error = True
        aux = hour.split(":")
        try:
            if int(aux[0]) < 24 and int(aux[0]) >= 0 and int(aux[1]) < 60 or int(aux[1]) >= 0:
                error = False
        except:
            pass
    return error

# Validate that returnTime be after departTime
def validate_depart_return(departTime, returnTime):
    error = False
    if departTime != "" and returnTime != "":
        aux_depart = departTime.split(":")
        aux_return = returnTime.split(":")
        try:
            if int(aux_depart[0]) > int(aux_return[0]):
                error = True
            elif int(aux_depart[0]) == int(aux_return[0]):
                if  int(aux_depart[1]) > int(aux_return[1]):
                    error = True
                elif int(aux_depart[1]) == int(aux_return[1]):
                    error = True
        except:
            error = True
    return error
