from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

from sharingcars.helpers.User import path_generator


APPLY_STATUS = (
    ('waiting', 'Waiting'),
    ('approach', 'Approach'),
    ('rejected', 'Rejected')
)


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
    biography = models.TextField(null=True)

    def delete(self):
        self.user_account.delete()
        return super(User, self).delete()

    def calculate_age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def get_rating(self):
        from routes.models import CommentRoute
        from announcements.models import CommentAnnouncement
        routes_rating_sum = CommentRoute.objects.filter(route__user=self).aggregate(models.Sum('rating')).get('rating__sum', 0)
        announcements_rating_sum = CommentAnnouncement.objects.filter(announcement__user=self).aggregate(models.Sum('rating')).get(
            'rating__sum', 0)
        user_rating_sum = Comment.objects.filter(evaluated=self).aggregate(models.Sum('rating')).get(
            'rating__sum', 0)
        rating_sum = 0
        if routes_rating_sum:
            rating_sum += routes_rating_sum
        if announcements_rating_sum:
            rating_sum += announcements_rating_sum
        if user_rating_sum:
            rating_sum += user_rating_sum
        rating_count = (CommentRoute.objects.filter(route__user=self).count() +
                        Comment.objects.filter(evaluated=self).count() +
                        CommentAnnouncement.objects.filter(announcement__user=self).count())
        if rating_count is 0:
            rating = 0
        else:
            rating = round(rating_sum / float(rating_count), 1)
        return rating

    def get_num_assessments(self):
        from routes.models import CommentRoute
        from announcements.models import CommentAnnouncement
        rating_count = (CommentRoute.objects.filter(route__user=self).count() +
                        Comment.objects.filter(evaluated=self).count() +
                        CommentAnnouncement.objects.filter(announcement__user=self).count())
        return rating_count

class Comment(models.Model):
    subject = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=False, max_length=395)
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
