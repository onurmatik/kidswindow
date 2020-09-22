from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.views.generic import TemplateView
from kidswindow.meetings.models import Meeting


DEFAULT_MEETING_DURATION_MINS = 120


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        meetings = Meeting.objects.filter(is_active=True, is_public=True)
        context.update({
            'now': now,
            'meetings_now': meetings.filter(
                time__lte=now,
                time__gt=now - timedelta(minutes=DEFAULT_MEETING_DURATION_MINS)
            ),
            'upcoming_games': meetings.filter(
                time__gte=now,
                type='g',
            ).filter().order_by('time')[:6],
            'upcoming_events': meetings.filter(
                time__gte=now,
                type='e',
            ).filter().order_by('time')[:6],
            'upcoming_tournaments': meetings.filter(
                time__gte=now,
                type='t',
            ).filter().order_by('time')[:6],
        })
        if not self.request.user.is_anonymous:
            meetings_user = Meeting.objects.filter(
                time__gt=now - timedelta(minutes=DEFAULT_MEETING_DURATION_MINS)
            ).filter(
                Q(host=self.request.user) | Q(participants=self.request.user)
            ).distinct().order_by('time')
            context.update({
                'meetings_user': meetings_user
            })
        return context
