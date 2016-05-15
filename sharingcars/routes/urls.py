from django.conf.urls import url
from routes.views import RouteCreateView, RouteListView
from routes.models import Route

urlpatterns = [
    url(r'^create$', RouteCreateView.as_view(), name='create-route'),
    url(r'^all$', RouteListView.as_view(queryset=Route.objects.order_by('-creationMoment')),
        name='all-routes'),
]
