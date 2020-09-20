from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, MeetingParticipant


def meeting_list(request):
    now = timezone.now()
    qs = Meeting.objects.filter(is_active=True, is_public=True)
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
        participation = MeetingParticipant.objects.filter(
            meeting=meeting,
            participant=request.user,
        ).first()
        context.update({
            'participation': participation
        })
    return render(request, 'meetings/meeting_detail.html', context)


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['game', 'time', 'notes']
        widgets = {
            'game': forms.Select(attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
            }),
            'time': forms.DateInput(attrs={'type':'datetime-local'}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
            }),
        }


@login_required
def meeting_create(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.host = request.user
            if request.user.profile.approved:
                meeting.is_active = True
            else:
                meeting.is_active = False
                send_mail(
                    'Yeni oyun',
                    render_to_string('meetings/email.html', {
                        'meeting': meeting,
                    }),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=settings.ADMIN_EMAILS,
                    fail_silently=True,
                )
            meeting.save()
            if meeting.is_active:
                messages.success(
                    request,
                    mark_safe(
                        f'Teşekkürler! Oyunun yayında. <a href="{meeting.get_absolute_url()}">Oyuna git!</a>'
                    )
                )
            else:
                messages.warning(
                    request,
                    'Teşekkürler! Oyununuz yöneticiler tarafından onaylandıktan sonra aktif hale gelecek.'
                )
            return redirect('index')
    else:
        form = MeetingForm()
    return render(request, 'meetings/form.html', {
        'form': form,
    })
