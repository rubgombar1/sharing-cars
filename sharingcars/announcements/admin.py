from django.contrib import admin
from announcements.models import (Announcement)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


admin.site.register(Announcement, AnnouncementAdmin)

# Register your models here.
