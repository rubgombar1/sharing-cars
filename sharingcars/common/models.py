from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

from sharingcars.helpers.User import path_generator


class Actor(models.Model):
    user_account = models.OneToOneField(DjangoUser, primary_key=True,
                                        on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user_account.username


class Administrator(Actor):
    pass


class User(Actor):
    name = models.CharField(max_length=256, blank=False)
    surnames = models.CharField(max_length=256, blank=False)
    city = models.CharField(max_length=256, blank=False)
    birthdate = models.DateField(blank=False)
    phone = models.CharField(max_length=256, blank=False,
                             validators=[RegexValidator('^\+?\d+$')])
    searchingCar = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=path_generator, null=True,
                              default='default')

    def delete(self):
        self.user_account.delete()
        return super(User, self).delete()


class Comment(models.Model):
    subject = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=False)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                 MaxValueValidator(10)])
    referrer = models.ForeignKey(User, related_name='referrer')
    evaluated = models.ForeignKey(User, related_name='evaluated')


class Folder(models.Model):
    name = models.CharField(max_length=256, blank=False)
    actor = models.ForeignKey(Actor)


class Message(models.Model):
    subject = models.CharField(max_length=256, blank=False)
    body = models.TextField(max_length=256, blank=False)
    creationMoment = models.DateTimeField(auto_now=False, auto_now_add=True)
    folder = models.ForeignKey(Folder)
    sender = models.ForeignKey(Actor, related_name='sender')
    recipient = models.ForeignKey(Actor, related_name='recipient')
