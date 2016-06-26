from django.conf.urls import url
from routes.views import (RouteCreateView, RouteUserListView,
                          RouteUserRecommendationsListView, RouteApplyCreate,
                          RouteDetailsView, resolve_apply)

from django.views.generic.list import ListView
from routes.models import Route

urlpatterns = [
    url(r'^create$', RouteCreateView.as_view(), name='create-route'),
    url(r'^all$', ListView.as_view(queryset=Route.objects.order_by('-creationMoment'),
                                   model=Route, template_name='routes/list.html'),
        name='all-routes'),
    url(r'^user$', RouteUserListView.as_view(), name='user-routes'),
    url(r'^recommendations$', RouteUserRecommendationsListView.as_view(), name='recommendations-routes'),
    url(r'^details/(?P<pk>[-\w]+)$', RouteDetailsView.as_view(),
        name='details-route'),
    url(r'^apply/(?P<pk>[-\w]+)$', RouteApplyCreate.as_view(), name='create-apply-route'),
    url(r'^apply/resolve/(?P<pk>[-\w]+)/(?P<action>[-\w]+)$', resolve_apply, name='resolve-apply-route'),
]
