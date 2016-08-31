"""sharingcars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from common.views import UserCreateView, UserProfileView, UserUpdateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='common/index.html'),
        name='index'),
    url(r'^login/?$', 'django.contrib.auth.views.login',
        {'template_name': 'common/registration/login.html'}, name="login"),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
    url(r'^user/register$', UserCreateView.as_view(), name='create-user'),
    url(r'^user/(?P<username>.*)/$', UserProfileView.as_view(), name='user-profile'),
    url(r'^user/(?P<username>.*)/update/', UserUpdateView.as_view(), name='user-update'),
    url(r'^messages/income/$', UserUpdateView.as_view(), name='messages-income'),
    url(r'^messages/outcome/$', UserUpdateView.as_view(), name='messages-outcome'),
    url(r'^messages/draft/$', UserUpdateView.as_view(), name='messages-draft'),
]
