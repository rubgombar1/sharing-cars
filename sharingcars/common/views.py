from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from common.models import User
from common.forms import UserRegisterForm


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url.format()
