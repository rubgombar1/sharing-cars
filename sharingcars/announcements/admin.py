from django.contrib import admin
from announcements.models import (Announcement, CommentAnnouncement, StopAnnouncement)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


class CommentAnnouncementAdmin(admin.ModelAdmin):
    pass


class StopAnnouncementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(StopAnnouncement, StopAnnouncementAdmin)
admin.site.register(CommentAnnouncement, CommentAnnouncementAdmin)
