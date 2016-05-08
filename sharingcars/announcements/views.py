from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from announcements.models import Announcement
# from common.forms import UserRegisterForm


class AnnouncementCreateView(CreateView):
    model = Announcement
    # form_class = UserRegisterForm
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')
    fields = ('origin', 'destination', 'description', 'kind',
              'seating', 'unitPrice', 'date', 'departTime')

    def get_success_url(self):
        return self.success_url.format()
