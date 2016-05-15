from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import User


class Route(models.Model):
    KINDS = (
        ('offer', _('Offer')),
        ('demand', _('Demand')),
    )
    origin = models.CharField(max_length=256, blank=False)
    destination = models.CharField(max_length=256, blank=False)
    visibility = models.BooleanField(default=True)
    description = models.TextField(blank=False)
    kind = models.CharField(max_length=64, choices=KINDS, blank=False)
    seating = models.IntegerField(validators=[MinValueValidator(0)],
                                  blank=False)
    unitPrice = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0)],
                                    blank=False)
    creationMoment = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User)


class ApplyRoute(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=False)
    state = models.CharField(max_length=64, default="1")

    route = models.ForeignKey(Route)
    user = models.ForeignKey(User)


class CommentRoute(models.Model):
    subject = models.CharField(max_length=128, blank=False)
    comment = models.TextField(blank=False)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                 MaxValueValidator(10)])
    user = models.ForeignKey(User)
    route = models.ForeignKey(Route)


class Day(models.Model):
    day = models.IntegerField()
    departTime = models.CharField(max_length=64)
    returnTime = models.CharField(max_length=64)
    active = models.BooleanField()
    route = models.ForeignKey(Route)


class StopRoute(models.Model):
    stop = models.CharField(max_length=256, blank=False)
    sequence = models.IntegerField(validators=[MinValueValidator(0)])
    route = models.ForeignKey(Route)
