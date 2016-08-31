from django.conf.urls import url
from routes.views import (RouteCreateView, RouteUserListView,
                          RouteUserRecommendationsListView, RouteApplyCreate,
                          RouteDetailsView, resolve_apply, RouteListView, RouteEditView)


urlpatterns = [
    url(r'^create$', RouteCreateView.as_view(), name='create-route'),
    url(r'^all$', RouteListView.as_view(), name='all-routes'),
    url(r'^user$', RouteUserListView.as_view(), name='user-routes'),
    url(r'^recommendations$', RouteUserRecommendationsListView.as_view(), name='recommendations-routes'),
    url(r'^details/(?P<pk>[-\w]+)$', RouteDetailsView.as_view(),
        name='details-route'),
    url(r'^apply/(?P<pk>[-\w]+)$', RouteApplyCreate.as_view(), name='create-apply-route'),
    url(r'^apply/resolve/(?P<pk>[-\w]+)/(?P<action>[-\w]+)$', resolve_apply, name='resolve-apply-route'),
    url(r'^edit/(?P<pk>[-\w]+)$', RouteEditView.as_view(),
        name='edit-route'),
]
