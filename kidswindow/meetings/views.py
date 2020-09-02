from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import forms
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, MeetingParticipant


def meeting_list(request):
    now = timezone.now()
    qs = Meeting.objects.exclude(cancelled=True)
    return render(request, 'index.html', {
        'now': qs.filter(time__lte=now, time__gt=now+timedelta(minutes=60)),
        'soon': qs.filter(time__gte=now)[:5],
    })


@login_required
def meeting_detail(request, meeting_slug):
    meeting = get_object_or_404(Meeting, slug=meeting_slug)
    meeting.participants.add(request.user)
    now = timezone.now()
    context = {
        'meeting': meeting,
    }
    if meeting.time < now < meeting.time + timedelta(hours=1):
        context.update({
            'meeting_status': 'NOW',
        })
    elif meeting.time > now:
        context.update({
            'meeting_status': 'WAIT',
        })
    else:
        meeting_next = Meeting.objects.filter(
            game=meeting.game,
            time__gte=now,
        ).order_by('time').first()
        context.update({
            'meeting_status': 'PASSED',
            'meeting_next': meeting_next,
        })

    if not request.user.is_anonymous:
        if meeting.time - timedelta(minutes=15) < now < meeting.time + timedelta(hours=1):
            if request.user in meeting.participants.all() and meeting.join_url:
                context.update({
                    'join_link_enabled': True,
                })
        participation = MeetingParticipant.objects.filter(
            meeting=meeting,
            participant=request.user,
        ).first()
        context.update({
            'participation': participation
        })
    return render(request, 'meetings/meeting_detail.html', context)
