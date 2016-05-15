from django.conf.urls import url
from routes.views import RouteCreateView

urlpatterns = [
    url(r'^create$', RouteCreateView.as_view(), name='create-route'),
]
