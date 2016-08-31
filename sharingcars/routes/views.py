from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from routes.models import Route, ApplyRoute
from common.models import User
from routes.forms import RouteCreateForm, ApplyRouteCreateForm


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


class RouteListView(ListView):
    queryset = Route.objects.filter(visibility=True).order_by('-creationMoment')
    model = Route
    template_name = 'routes/list.html'


class RouteDetailsView(DetailView):
    template_name = 'routes/show.html'
    queryset = Route.objects.filter(visibility=True)


class RouteUserListView(ListView):
    model = Route
    template_name = 'routes/list.html'

    def get_queryset(self):
        return Route.objects.filter(user__user_account__id=self.request.user.id, visibility=True)


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


class RouteApplyCreate(CreateView):
    model = ApplyRoute
    template_name = 'common/form.html'
    form_class = ApplyRouteCreateForm

    def get_success_url(self):
        return reverse('details-route', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        route = Route.objects.get(pk=self.kwargs['pk'])
        instance.user = user
        instance.route = route
        return super(RouteApplyCreate, self).form_valid(form)


@login_required
def resolve_apply(request, pk, action):
    apply_route = ApplyRoute.objects.get(pk=pk)
    if action == 'approach':
        apply_route.state = 'approach'
    elif action == 'reject':
        apply_route.state = 'rejected'
    apply_route.save()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('details-route', pk=apply_route.route.pk)
