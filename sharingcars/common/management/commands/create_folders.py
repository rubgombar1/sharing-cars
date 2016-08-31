# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib import auth
from datetime import date, datetime
from common.models import (User, Folder)


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        for user in User.objects.all():
            Folder.objects.get_or_create(name='Bandeja de entrada', actor=user)
            Folder.objects.get_or_create(name='Bandeja de salida', actor=user)
            Folder.objects.get_or_create(name='Papelera', actor=user)

    def handle(self, *args, **options):
        self._migrate()
