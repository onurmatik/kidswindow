import secrets
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from kidswindow.games.models import Game


class Meeting(models.Model):
    slug = models.SlugField(blank=True, null=True, editable=False)
    game = models.ForeignKey(Game, verbose_name=_('game'), on_delete=models.CASCADE)
    time = models.DateTimeField(_('time'))
    notes = models.TextField(blank=True, null=True)
    host = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='hosted_meetings',
        verbose_name=_('meeting host'),
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        through='MeetingParticipant',
        related_name='participated_meetings',
        verbose_name=_('participants'),
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return str(_(self.game.name))

    def get_absolute_url(self):
        return reverse('meeting_detail', kwargs={
            'meeting_slug': self.slug
        })

    def save(self, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(16).lower()
        super().save(**kwargs)

    class Meta:
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('participant'))
    tutor = models.BooleanField(_('co-host'), default=False)
    joined = models.DateTimeField(_('time joined'), auto_now_add=True)

    class Meta:
        unique_together = (('meeting', 'participant'),)
        verbose_name = _('meeting participant')
        verbose_name_plural = _('meeting participants')


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

    class Meta:
        verbose_name = _('meeting poll')
        verbose_name_plural = _('meeting polls')
