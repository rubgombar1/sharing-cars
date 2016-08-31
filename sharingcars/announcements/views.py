from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from announcements.models import Announcement, ApplyAnnouncement, StopAnnouncement
from common.models import User
from announcements.forms import AnnouncementCreateForm, ApplyAnnouncementCreateForm, StopAnnouncementForm


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
        return Announcement.objects.filter(user__user_account__id=self.request.user.id)


class ApplyAnnouncementsUser(ListView):
    model = ApplyAnnouncement
    template_name = 'common/apply/list.html'

    def get_queryset(self):
        return ApplyAnnouncement.objects.filter(~Q(state='rejected'),
                                                announcement__user__user_account__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ApplyAnnouncementsUser, self).get_context_data(**kwargs)
        context['title'] = u'Solicitudes de anuncios recibidas'
        context['kind_apply'] = u'Ir al anuncio'
        return context



class AnnouncementApplyCreate(CreateView):
    model = ApplyAnnouncement
    template_name = 'common/form.html'
    form_class = ApplyAnnouncementCreateForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        instance.user = user
        instance.announcement = announcement
        return super(AnnouncementApplyCreate, self).form_valid(form)


@login_required
def resolve_apply(request, pk, action):
    apply_announcement = ApplyAnnouncement.objects.get(pk=pk)
    if action == 'approach':
        apply_announcement.state = 'approach'
    elif action == 'reject':
        apply_announcement.state = 'rejected'
    apply_announcement.save()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('details-announcement', pk=apply_announcement.announcement.pk)


class AnnouncementDetailsView(DetailView):
    template_name = 'announcements/announcement/show.html'
    model = Announcement

    def get_queryset(self):
        return Announcement.objects.filter(Q(visibility=True) | Q(user__user_account__pk=self.request.user.pk))


class EditAnnouncementView(UpdateView):
    model = Announcement
    template_name = 'announcements/announcement/create.html'
    success_url = reverse_lazy('index')
    form_class = AnnouncementCreateForm

    def get_success_url(self):
        return self.success_url.format()


class StopAnnouncementCreateView(CreateView):
    model = StopAnnouncement
    template_name = 'announcements/stop/create.html'
    success_url = reverse_lazy('index')
    form_class = StopAnnouncementForm

    def get_success_url(self):
        return self.success_url.format()

    def form_valid(self, form):
        instance = form.save(commit=False)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        instance.announcement = announcement
        return super(StopAnnouncementCreateView, self).form_valid(form)