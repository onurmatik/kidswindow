import secrets
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from kidswindow.games.models import Game


class Meeting(models.Model):
    game = models.ForeignKey(Game, verbose_name=_('game'), on_delete=models.CASCADE)
    time = models.DateTimeField(_('time'))
    topic = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    host = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='hosted_meetings',
        verbose_name=_('meeting host'),
    )
    start_url = models.URLField(_('Start URL'), blank=True, null=True)
    join_url = models.URLField(_('Join URL'), blank=True, null=True)
    participants = models.ManyToManyField(
        User,
        blank=True,
        through='MeetingParticipant',
        related_name='participated_meetings',
        verbose_name=_('participants'),
    )
    type = models.PositiveSmallIntegerField(_('meeting type'), choices=(
        (1, _('play')),
        (2, _('community meeting')),
    ), default=1)
    cancelled = models.BooleanField(default=False)
    cancellation_reason = models.PositiveSmallIntegerField(blank=True, null=True, choices=(
        (1, _('no host')),
        (2, _('no participant')),
        (0, _('other')),
    ))

    def __str__(self):
        return str(_(self.game.name))

    def get_absolute_url(self):
        return reverse('meeting_detail', kwargs={
            'meeting_id': self.id
        })

    def save(self, **kwargs):
        if not self.start_url:
            # create a random Jitsi meeting link
            uri = _('KidsWindow_%(game)s_%(code)s') % {
                'game': self.game.name.upper(),
                'code': secrets.token_urlsafe(8).lower(),
            }
            self.join_url = self.start_url = 'https://meet.jit.si/%s' % uri
        super().save(**kwargs)

    def clean(self):
        # TODO: check for overlaps
        pass


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('participant'))
    tutor = models.BooleanField(_('co-host'), default=False)
    joined = models.DateTimeField(_('time joined'), auto_now_add=True)

    class Meta:
        unique_together = (('meeting', 'participant'),)


class MeetingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name=_('game'))
    tutor = models.BooleanField(_('co-host'), default=False, choices=(
        (False, _('participant')),
        (True, _('co-host')),
    ))
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)


class MeetingPoll(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    rate = models.PositiveSmallIntegerField(_('rate'), choices=(
        (1, _('Poor')),
        (2, _('OK')),
        (3, _('Good')),
    ))
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)
