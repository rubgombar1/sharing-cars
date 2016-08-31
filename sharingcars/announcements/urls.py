from django.conf.urls import url
from announcements.views import (AnnouncementCreateView, AnnouncementListView, AnnouncementUserListView,
                                 ApplyAnnouncementsUser, AnnouncementApplyCreate, resolve_apply,
                                 AnnouncementDetailsView)

urlpatterns = [
    url(r'^create$', AnnouncementCreateView.as_view(), name='create-announcement'),
    url(r'^all', AnnouncementListView.as_view(), name='announcement-all'),
    url(r'^user', AnnouncementUserListView.as_view(), name='announcement-user'),
    url(r'^apply/received$', ApplyAnnouncementsUser.as_view(), name='apply-announcement-user-received'),
    url(r'^apply/(?P<pk>[-\w]+)$', AnnouncementApplyCreate.as_view(), name='create-apply-announcement'),
    url(r'^apply/resolve/(?P<pk>[-\w]+)/(?P<action>[-\w]+)$', resolve_apply, name='resolve-apply-announcement'),
    url(r'^details/(?P<pk>[-\w]+)$', AnnouncementDetailsView.as_view(),
        name='details-announcement'),
]
