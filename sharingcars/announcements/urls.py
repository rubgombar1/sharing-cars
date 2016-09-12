from django.conf.urls import url
from announcements.views import (AnnouncementCreateView, AnnouncementListView, AnnouncementUserListView,
                                 ApplyAnnouncementsReceivedUser, AnnouncementApplyCreate, resolve_apply,
                                 AnnouncementDetailsView, EditAnnouncementView, StopAnnouncementCreateView,
                                 StopAnnouncementUpdateView, ApplyAnnouncementsPerformedUser, AnnouncementApplyDelete,
                                 AnnouncementUserRecommendationsListView, CommentAnnouncementCreateView)

urlpatterns = [
    url(r'^create$', AnnouncementCreateView.as_view(), name='create-announcement'),
    url(r'^all', AnnouncementListView.as_view(), name='announcement-all'),
    url(r'^user', AnnouncementUserListView.as_view(), name='announcement-user'),
    url(r'^apply/received$', ApplyAnnouncementsReceivedUser.as_view(), name='apply-announcement-user-received'),
    url(r'^apply/performed$', ApplyAnnouncementsPerformedUser.as_view(), name='apply-announcement-user-performed'),
    url(r'^apply/(?P<pk>[-\w]+)$', AnnouncementApplyCreate.as_view(), name='create-apply-announcement'),
    url(r'^apply/remove/(?P<pk>[-\w]+)$', AnnouncementApplyDelete.as_view(), name='remove-apply-announcement'),
    url(r'^apply/resolve/(?P<pk>[-\w]+)/(?P<action>[-\w]+)$', resolve_apply, name='resolve-apply-announcement'),
    url(r'^details/(?P<pk>[-\w]+)$', AnnouncementDetailsView.as_view(),
        name='details-announcement'),
    url(r'^edit/(?P<pk>[-\w]+)$', EditAnnouncementView.as_view(),
            name='edit-announcement'),
    url(r'^stop/create/(?P<pk>[-\w]+)$', StopAnnouncementCreateView.as_view(),
            name='stop-announcement-create'),
    url(r'^stop/edit/(?P<pk>[-\w]+)$', StopAnnouncementUpdateView.as_view(),
            name='stop-announcement-edit'),
    url(r'^recommendations$', AnnouncementUserRecommendationsListView.as_view(), name='recommendations-announcements'),
    url(r'^comment/create/(?P<announcement_pk>[-\w]+)$', CommentAnnouncementCreateView.as_view(), name='create-comment-announcement'),
]
