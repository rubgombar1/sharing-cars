from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from announcements.models import Announcement
from common.models import User
# from common.forms import UserRegisterForm


class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = 'common/registration/register.html'
    success_url = reverse_lazy('index')
    fields = ('origin', 'destination', 'description', 'kind',
              'seating', 'unitPrice', 'date', 'departTime')

    def get_success_url(self):
        return self.success_url.format()

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        instance.user = user
        return super(AnnouncementCreateView, self).form_valid(form)
