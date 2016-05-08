from django.contrib import admin
from announcements.models import (Announcement)


class AnnouncementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Announcement, AnnouncementAdmin)

# Register your models here.
