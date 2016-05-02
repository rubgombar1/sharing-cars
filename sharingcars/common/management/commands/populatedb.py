# 'manage.py populatedb'
# -*- coding: utf-8 -*-
#
from django.core.management.base import BaseCommand
from django.contrib import auth
from datetime import date, datetime
from common.models import (Administrator, User, Message, Folder, Comment)
from announcements.models import (Announcement, ApplyAnnouncement,
                                  CommentAnnouncement, StopAnnouncement)
from routes.models import (ApplyRoute, CommentRoute, Day, Route, StopRoute)


class AppluRoute(object):
    pass


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        auth.models.User.objects.all().delete()
        Administrator.objects.all().delete()
        User.objects.all().delete()
        Folder.objects.all().delete()
        Message.objects.all().delete()
        Announcement.objects.all().delete()
        ApplyAnnouncement.objects.all().delete()
        ApplyRoute.objects.all().delete()
        Comment.objects.all().delete()
        CommentAnnouncement.objects.all().delete()
        CommentRoute.objects.all().delete()
        Day.objects.all().delete()
        Route.objects.all().delete()
        StopAnnouncement.objects.all().delete()
        StopRoute.objects.all().delete()

        print("Dropping tables OK!")

        print('Create administrators accounts...')
        admin1 = auth.models.User.objects.create_superuser(username='admin', email='admin@sharingcar.com',
                                                                   password='admin')

        print('Create administrators accounts OK!')

        print('Create users accounts...')
        user_account1 = auth.models.User.objects.create_user(username='user1', email='user1@user.com',
                                                                   password='user')

        user_account2 = auth.models.User.objects.create_user(username='user2', email='user2@user.com',
                                                                   password='user')
        print('Create users accounts OK!')

        print('Create administrators...')
        administrator = Administrator(user_account = admin1)
        administrator.save()

        print('Create administrators OK!')

        print('Create users...')
        user1 = User(user_account = user_account1,name = "Nombre", surnames = "Apellido1 Apellido2", city = "Sevilla",
                     birthdate = date(1993, 4, 6), phone = "666999888",searchinCar = True)
        user1.save()
        user2 = User(user_account = user_account2,name = "Nombre2", surnames = "Apellido1 Apellido2", city = "Sevilla",
                     birthdate = date(1993, 4, 6), phone = "666999888",searchinCar = True)
        user2.save()
        print('Create user OK!')

        print('Create folders...')
        folder1 = Folder(name = "1", actor = user1)
        folder1.save()
        folder2 = Folder(name = "2", actor = user1)
        folder2.save()
        folder3 = Folder(name = "3", actor = user1)
        folder3.save()

        folder4 = Folder(name = "1", actor = user2)
        folder4.save()
        folder5 = Folder(name = "2", actor = user2)
        folder5.save()
        folder6 = Folder(name = "3", actor = user2)
        folder6.save()

        folder7 = Folder(name = "1", actor = administrator)
        folder7.save()
        folder8 = Folder(name = "2", actor = administrator)
        folder8.save()
        folder9 = Folder(name = "3", actor = administrator)
        folder9.save()

        print('Create folders OK!')

        print('Create messages...')
        message1 = Message(subject = "Asunto 1", body = "Este es un mensaje de prueba enviado", folder = folder1, sender = user1,
                           recipient = user2)
        message1.save()
        message2 = Message(subject = "Asunto 1", body = "Este es un mensaje de prueba enviado", folder = folder5, sender = user1,
                           recipient = user2)
        message2.save()

        print('Create messages OK!')

        print('Create comments...')
        comment1 = Comment(subject = "Muy bueno", comment = "Muy buen conductor, totalmente recomendable", rating = 9, referrer = user1,
                           evaluated = user2)
        comment1.save()
        comment2 = Comment(subject = "Regular", comment = "Como pasajero deja mucho que desear", rating = 4, referrer = user2,
                           evaluated = user1)
        comment2.save()

        print('Create comments OK!')

        print('Create routes...')
        route1 = Route(origin = "Alcalá de Guadaíra", destination = "Facultad de Informática", description = "Viaje regular durante 3 meses",
                           kind = "1", seating = 4, unitPrice = 2.00, user = user2)
        route1.save()
        route2 = Route(origin = "Arahal", destination = "Isla de la cartuja", description = "Viaje regular durante 6 meses",
                           kind = "1", seating = 4, unitPrice = 2.00, user = user1)
        route2.save()
        print('Create routes OK!')

        print('Create stop routes...')

        stopRoute1 = StopRoute(stop = "Alcalá de Guadaíra", sequence = 1, route = route2)
        stopRoute1.save()

        print('Create stop routes OK!')

        print('Create days...')

        day1 = Day(day = 1, departTime = "7:55", returnTime = "14:00", route = route2, active = True)
        day1.save()
        day2 = Day(day = 2, departTime = "7:55", returnTime = "14:00", route = route2, active = True)
        day2.save()
        day3 = Day(day = 3, departTime = "7:55", returnTime = "14:00", route = route2, active = True)
        day3.save()
        day4 = Day(day = 4, departTime = "7:55", returnTime = "14:00", route = route2, active = True)
        day4.save()
        day5 = Day(day = 5, departTime = "7:55", returnTime = "14:00", route = route2, active = True)
        day5.save()
        day6 = Day(day = 6, route = route2, active = False)
        day6.save()
        day7 = Day(day = 7, route = route2, active = False)
        day7.save()

        day8 = Day(day = 1, departTime = "7:55", returnTime = "14:00", route = route1, active = True)
        day8.save()
        day9 = Day(day = 2, departTime = "7:55", returnTime = "14:00", route = route1, active = True)
        day9.save()
        day10 = Day(day = 3, departTime = "7:55", returnTime = "14:00", route = route1, active = True)
        day10.save()
        day11 = Day(day = 4, departTime = "7:55", returnTime = "14:00", route = route1, active = True)
        day11.save()
        day12 = Day(day = 5, departTime = "7:55", returnTime = "14:00", route = route1, active = True)
        day12.save()
        day13 = Day(day = 6, route = route1, active = False)
        day13.save()
        day14 = Day(day = 7, route = route1, active = False)
        day14.save()

        print('Create days OK!')

        print('Create applys routes...')

        applyRoute1 = ApplyRoute(comment = "Buenas, yo entro a las 9 de la mañana y salgo a las dos, te viene bien en Alcalá de Guadaíra?",
                                 route= route2, user = user1)
        applyRoute1.save()

        print('Create applys routes OK!')

        print('Create comments  routes...')

        commentRoute1 = CommentRoute(subject = "Buena ruta!", comment = "Muy buen trayecto, excelente conductor", rating = 10,
                                     user = user1, route = route2)
        commentRoute1.save()

        print('Create comments routes OK!')

        print('Create announcements ...')
        announcement1 = Announcement(origin = "Alcalá de Guadaíra", destination = "Facultad de informática", description = "Viaje puntual"
                                     , seating = 2, unitPrice = 2, date = datetime(2015, 12, 6, 16, 29, 43, 79043), user = user1)
        announcement1.save()
        print('Create announcements OK!')

        print('Create applys  announcements...')
        applyAnnouncement1 = ApplyAnnouncement(comment = "Buenas, yo entro a las 17:00 de la tarde te viene bien los arcos?",
                                               announcement=announcement1, user=user1)
        applyAnnouncement1.save()
        print('Create applys announcements OK!')

        print('Create stops  announcements...')
        stopAnnouncement1 = StopAnnouncement(stop = "Sevilla", sequence = 1, announcement = announcement1)
        stopAnnouncement1.save()
        print('Create stops announcements OK!')

        print('Create comments  announcements...')
        commentAnnouncement1 = CommentAnnouncement(subject = "Buena ruta!", comment = "Muy buen trayecto, excelente conductor", rating = 10,
                                     user = user1, announcement = announcement1)
        commentAnnouncement1.save()
        print('Create comments announcements OK!')

    def handle(self, *args, **options):
        self._migrate()
