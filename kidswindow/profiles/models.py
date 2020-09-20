from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from kidswindow.games.models import Game
from kidswindow.meetings.models import Meeting, MeetingParticipant


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    birth_year = models.PositiveSmallIntegerField(blank=True, null=True)
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @cached_property
    def games(self):
        meeting_ids = MeetingParticipant.objects.filter(participant=self.user).values_list('meeting', flat=True)
        game_ids = Meeting.objects.filter(id__in=meeting_ids).values_list('game', flat=True)
        return Game.objects.filter(id__in=game_ids)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


def create_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(
        user=instance,
    )
models.signals.post_save.connect(create_profile, sender=User)
