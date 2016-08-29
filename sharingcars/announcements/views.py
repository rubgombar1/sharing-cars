from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView

from announcements.models import Announcement, ApplyAnnouncement
from common.models import User
from announcements.forms import AnnouncementCreateForm


class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = 'announcements/announcement/create.html'
    success_url = reverse_lazy('index')
    form_class = AnnouncementCreateForm

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


class ApplyAnnouncementsUser(ListView):
    model = ApplyAnnouncement
    template_name = 'announcements/apply/list.html'

    def get_queryset(self):
        return ApplyAnnouncement.objects.filter(announcement__user__user_account__id=self.request.user.id)


class AnnouncementApplyCreate(CreateView):
    model = ApplyAnnouncement
    template_name = 'common/form.html'
    fields = ['comment']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        instance.user = user
        instance.announcement = announcement
        return super(AnnouncementApplyCreate, self).form_valid(form)