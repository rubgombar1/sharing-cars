from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from common.models import User


class Announcement(models.Model):
    KINDS = (
        ('offer', 'Offer'),
        ('demand', 'Demand'),
    )
    origin = models.CharField(max_length=256, blank=False)
    destination = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    kind = models.CharField(max_length=64, choices=KINDS, blank=False)
    seating = models.IntegerField(validators=[MinValueValidator(0)],
                                  blank=False)
    unitPrice = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0)],
                                    blank=False)
    date = models.DateField(blank=False)
    creationMoment = models.DateTimeField(auto_now=False, auto_now_add=True)
    departTime = models.CharField(max_length=64)

    user = models.OneToOneField(User)

    def __unicode__(self):
        return '%s - %s - %s' % (self.origin, self.destination, self.departTime)


class ApplyAnnouncement(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=False)
    state = models.CharField(max_length=64, default="1")

    announcement = models.OneToOneField(Announcement)
    user = models.OneToOneField(User)


class CommentAnnouncement(models.Model):
    subject = models.CharField(max_length=128, blank=False)
    comment = models.TextField(blank=False)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                 MaxValueValidator(10)])
    user = models.OneToOneField(User)
    announcement = models.OneToOneField(Announcement)


class StopAnnouncement(models.Model):
    stop = models.CharField(max_length=256, blank=False)
    sequence = models.IntegerField(validators=[MinValueValidator(0)])
    announcement = models.ForeignKey(Announcement)
