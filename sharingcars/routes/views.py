from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView

from routes.models import Route, ApplyRoute, StopRoute
from common.models import User
from routes.forms import RouteCreateForm, ApplyRouteCreateForm, RouteEditForm, StopRouteForm



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


class RouteEditView(UpdateView):
    model = Route
    form_class = RouteEditForm
    template_name = 'routes/create.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url.format()

    def get_initial(self):
        initial = super(RouteEditView, self).get_initial()
        for day in self.object.day_set.all():
            if day.day == 1:
                initial['monday_departTime'] = day.departTime
                initial['monday_returnTime'] = day.returnTime
            elif day.day == 2:
                initial['tuesday_departTime'] = day.departTime
                initial['tuesday_returnTime'] = day.returnTime
            elif day.day == 3:
                initial['wednesday_departTime'] = day.departTime
                initial['wednesday_returnTime'] = day.returnTime
            elif day.day == 4:
                initial['thursday_departTime'] = day.departTime
                initial['thursday_returnTime'] = day.returnTime
            elif day.day == 5:
                initial['friday_departTime'] = day.departTime
                initial['friday_returnTime'] = day.returnTime
            elif day.day == 6:
                initial['saturday_departTime'] = day.departTime
                initial['saturday_returnTime'] = day.returnTime
            elif day.day == 7:
                initial['sunday_departTime'] = day.departTime
                initial['sunday_returnTime'] = day.returnTime
        return initial


class RouteListView(ListView):
    model = Route
    template_name = 'routes/list.html'

    def get_queryset(self):
        return Route.objects.filter(visibility=True).order_by('-creationMoment')


class RouteDetailsView(DetailView):
    template_name = 'routes/show.html'

    def get_queryset(self):
        return Route.objects.filter(Q(visibility=True) | Q(user__user_account__pk=self.request.user.pk))


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
    apply_route.route.check_applies()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('details-route', pk=apply_route.route.pk)


class StopRouteCreateView(CreateView):
    model = StopRoute
    template_name = 'routes/stop/create.html'
    success_url = reverse_lazy('index')
    form_class = StopRouteForm

    def get_success_url(self):
        return self.success_url.format()

    def form_valid(self, form):
        instance = form.save(commit=False)
        route = Route.objects.get(pk=self.kwargs['pk'])
        instance.route = route
        return super(StopRouteCreateView, self).form_valid(form)


class StopRouteUpdateView(UpdateView):
    model = StopRoute
    template_name = 'routes/stop/create.html'
    success_url = reverse_lazy('index')
    form_class = StopRouteForm

    def get_success_url(self):
        return self.success_url.format()


class ApplyRouteReceivedUser(ListView):
    model = ApplyRoute
    template_name = 'routes/apply/list.html'

    def get_queryset(self):
        return ApplyRoute.objects.filter(~Q(state='rejected'),
                                         route__user__user_account__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ApplyRouteReceivedUser, self).get_context_data(**kwargs)
        context['title'] = u'Solicitudes de rutas recibidas'
        context['kind_apply'] = u'Ir a la ruta'
        context['received'] = True
        return context


class ApplyRoutePerformedUser(ListView):
    model = ApplyRoute
    template_name = 'routes/apply/list.html'

    def get_queryset(self):
        return ApplyRoute.objects.filter(user__user_account__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ApplyRoutePerformedUser, self).get_context_data(**kwargs)
        context['title'] = u'Solicitudes de rutas realizadas'
        context['kind_apply'] = u'Ir a la ruta'
        return context


class RouteApplyDelete(DeleteView):
    model = ApplyRoute
    success_url = reverse_lazy('index')

    def get_queryset(self):
        qs = super(RouteApplyDelete, self).get_queryset()
        return qs.filter(~Q(state='approach'), user__user_account=self.request.user)