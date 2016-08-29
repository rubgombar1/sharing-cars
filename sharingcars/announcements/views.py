from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView

from announcements.models import Announcement
from common.models import User


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


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement/list.html'

    def get_queryset(self):
        return Announcement.objects.filter(visibility=True)


class AnnouncementUserListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement/list.html'

    def get_queryset(self):
        return Announcement.objects.filter(visibility=True, user__user_account__id=self.request.user.id)