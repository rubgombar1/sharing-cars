from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from routes.models import Route
from common.models import User
from routes.forms import RouteCreateForm


class RouteCreateView(CreateView):
    model = Route
    form_class = RouteCreateForm
    template_name = 'routes/create.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url.format()

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        instance.user = user
        return super(RouteCreateView, self).form_valid(form)


class RouteUserListView(ListView):
    model = Route
    template_name = 'routes/list.html'

    def get_queryset(self):
        return Route.objects.filter(user__user_account__id=self.request.user.id)


class RouteUserRecommendationsListView(ListView):
    model = Route
    template_name = 'routes/list.html'

    def get_context_data(self):
        context = super(RouteUserRecommendationsListView, self).get_context_data()
        userId = self.request.user.id
        userRoutes = Route.objects.filter(user__user_account__id=userId)
        routes = Route.objects.filter(~Q(user__user_account__id=userId), visibility=1)
        recommendations = set()
        for userRoute in userRoutes:
            for route in routes:
                if userRoute.origin == route.origin and userRoute.destination == route.destination:
                    recommendations.add(route)
        context['route_list'] = recommendations
        return context
