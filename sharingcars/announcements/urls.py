from django.conf.urls import url
from announcements.views import (AnnouncementCreateView, AnnouncementListView, AnnouncementUserListView,
                                 ApplyAnnouncementsUser, AnnouncementApplyCreate)

urlpatterns = [
    url(r'^create$', AnnouncementCreateView.as_view(), name='create-announcement'),
    url(r'^all', AnnouncementListView.as_view(), name='announcement-all'),
    url(r'^user', AnnouncementUserListView.as_view(), name='announcement-user'),
    url(r'^apply/received$', ApplyAnnouncementsUser.as_view(), name='apply-announcement-user-received'),
    url(r'^apply/(?P<pk>[-\w]+)$', AnnouncementApplyCreate.as_view(), name='create-apply-announcement'),
]
