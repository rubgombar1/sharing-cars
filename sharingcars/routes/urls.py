from django.conf.urls import url
from routes.views import RouteCreateView, RouteUserListView, RouteUserRecommendationsListView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from routes.models import Route

urlpatterns = [
    url(r'^create$', RouteCreateView.as_view(), name='create-route'),
    url(r'^all$', ListView.as_view(queryset=Route.objects.order_by('-creationMoment'),
                                   model=Route, template_name='routes/list.html'),
        name='all-routes'),
    url(r'^user$', RouteUserListView.as_view(), name='user-routes'),
    url(r'^recommendations$', RouteUserRecommendationsListView.as_view(), name='recommendations-routes'),
    url(r'^details/(?P<pk>[-\w]+)$', DetailView.as_view(template_name='routes/show.html',
                                                        queryset=Route.objects.all()),
        name='details-route'),
]
