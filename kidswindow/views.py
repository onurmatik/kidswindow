from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.generic import TemplateView
from kidswindow.meetings.models import Meeting


DEFAULT_MEETING_DURATION_MINS = 120


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        meetings = Meeting.objects.all()
        context.update({
            'meeting_now':meetings.filter(
                time__lte=now,
                time__gt=now - timedelta(minutes=DEFAULT_MEETING_DURATION_MINS)
            ).first(),
            'meetings_soon': meetings.filter(time__gte=now).filter(is_public=True).order_by('time')[:6],
            'meetings_community': meetings.filter(time__gte=now).filter(is_public=True).order_by('time')[:6],
            'now': now,
        })
        if not self.request.user.is_anonymous:
            qs = Meeting.objects.filter(
                time__gt=timezone.now() - timedelta(minutes=DEFAULT_MEETING_DURATION_MINS)
            )
            context.update({
                'meetings_user': qs.filter(
                    participants=self.request.user
                ).distinct().order_by('time'),
                'meetings_suggested': qs.filter(
                    game__in=self.request.user.profile.games.all()
                ).exclude(
                    participants=self.request.user
                ).order_by('time'),
            })
        return context


def set_language(request):
    next_page = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(next_page) if next_page else HttpResponseRedirect('/')
    lang_code = request.GET.get('lang')
    next_trans = translate_url(next_page, lang_code)
    if next_trans != next_page:
        response = HttpResponseRedirect(next_trans)
    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = lang_code
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
    )
    return response
