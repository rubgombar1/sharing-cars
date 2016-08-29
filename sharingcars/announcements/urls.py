from django.conf.urls import url
from announcements.views import (AnnouncementCreateView, AnnouncementListView, AnnouncementUserListView)

urlpatterns = [
    url(r'^create$', AnnouncementCreateView.as_view(), name='create-announcement'),
    url(r'^all', AnnouncementListView.as_view(), name='announcement-all'),
    url(r'^user', AnnouncementUserListView.as_view(), name='announcement-user'),
]
