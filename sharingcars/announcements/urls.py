from django.conf.urls import url
from announcements.views import AnnouncementCreateView

urlpatterns = [
    url(r'^create$', AnnouncementCreateView.as_view(), name='create-announcement'),
]
