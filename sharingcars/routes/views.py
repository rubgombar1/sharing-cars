from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy

from routes.models import Route
from common.models import User
from routes.forms import RouteCreateForm


class RouteCreateView(CreateView):
    model = Route
    form_class = RouteCreateForm
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url.format()

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        instance.user = user
        return super(RouteCreateView, self).form_valid(form)


class RouteListView(ListView):
    template_name = 'routes/list.html'
    model = Route
