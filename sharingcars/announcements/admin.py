from django.contrib import admin
from announcements.models import (Announcement, CommentAnnouncement, StopAnnouncement, ApplyAnnouncement)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


class CommentAnnouncementAdmin(admin.ModelAdmin):
    pass


class StopAnnouncementAdmin(admin.ModelAdmin):
    pass


class ApplyAnnouncementAdmin(admin.ModelAdmin):
    pass


admin.site.register(ApplyAnnouncement, ApplyAnnouncementAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(StopAnnouncement, StopAnnouncementAdmin)
admin.site.register(CommentAnnouncement, CommentAnnouncementAdmin)
