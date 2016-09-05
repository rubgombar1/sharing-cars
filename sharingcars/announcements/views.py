from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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


class ApplyAnnouncementsReceivedUser(ListView):
    model = ApplyAnnouncement
    template_name = 'announcements/apply/list.html'

    def get_queryset(self):
        return ApplyAnnouncement.objects.filter(~Q(state='rejected'),
                                                announcement__user__user_account__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ApplyAnnouncementsReceivedUser, self).get_context_data(**kwargs)
        context['title'] = u'Solicitudes de anuncios recibidas'
        context['kind_apply'] = u'Ir al anuncio'
        context['received'] = True
        return context



class AnnouncementApplyCreate(LoginRequiredMixin, CreateView):
    model = ApplyAnnouncement
    template_name = 'common/form.html'
    form_class = ApplyAnnouncementCreateForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        user = User.objects.get(user_account__id=self.request.user.id)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        instance.user = user
        instance.announcement = announcement
        return super(AnnouncementApplyCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            user = User.objects.get(user_account__id=self.request.user.id)
            announcement = Announcement.objects.get(pk=self.kwargs['pk'])
            if announcement.applyannouncement_set.filter(user=user).exists():
                previous_url = self.request.META.get('HTTP_REFERER', None)
                messages.add_message(self.request, messages.ERROR,
                                     'Ya tiene una solicitud para este anuncio')

                if previous_url:
                    return redirect(previous_url)
                else:
                    return redirect('announcement-all')
        return super(AnnouncementApplyCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('details-announcement', kwargs={'pk': self.kwargs['pk']})

@login_required
def resolve_apply(request, pk, action):
    apply_announcement = ApplyAnnouncement.objects.get(pk=pk)
    if action == 'approach':
        if apply_announcement.announcement.get_seats_free() > 0:
            apply_announcement.state = 'approach'
        else:
            previous_url = request.META.get('HTTP_REFERER', None)
            messages.add_message(request, messages.ERROR, 'No puede aceptar esta solicitud porque no hay asientos libres')
            return redirect(previous_url)
    elif action == 'reject':
        apply_announcement.state = 'rejected'
    apply_announcement.save()
    apply_announcement.announcement.check_applies()
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


class StopAnnouncementUpdateView(UpdateView):
    model = StopAnnouncement
    template_name = 'announcements/stop/create.html'
    success_url = reverse_lazy('index')
    form_class = StopAnnouncementForm

    def get_success_url(self):
        return self.success_url.format()


class ApplyAnnouncementsPerformedUser(ListView):
    model = ApplyAnnouncement
    template_name = 'announcements/apply/list.html'

    def get_queryset(self):
        return ApplyAnnouncement.objects.filter(user__user_account__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ApplyAnnouncementsPerformedUser, self).get_context_data(**kwargs)
        context['title'] = u'Solicitudes de anuncios realizadas'
        context['kind_apply'] = u'Ir al anuncio'
        return context


class AnnouncementApplyDelete(DeleteView):
    model = ApplyAnnouncement
    success_url = reverse_lazy('index')

    def get_queryset(self):
        qs = super(AnnouncementApplyDelete, self).get_queryset()
        return qs.filter(~Q(state='approach'), user__user_account=self.request.user)