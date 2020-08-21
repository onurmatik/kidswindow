from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneField
from kidswindow.games.models import Game


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    timezone = TimeZoneField(_('timezone'), blank=True, null=True)
    games = models.ManyToManyField(
        Game,
        through='ProfileGame',
        blank=True,
        verbose_name=_('games')
    )
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)

    def __str__(self):
        return self.user.username


class ProfileGame(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name=_('profile')
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name=_('game')
    )
    tutor = models.BooleanField(_('tutor'), default=False)
    time = models.DateTimeField(_('time'), auto_now_add=True)

    def __str__(self):
        return str(_(self.game.name))

    class Meta:
        unique_together = (('profile', 'game'),)


class Report(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_set',
        verbose_name=_('reported by')
    )
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(
        user=instance,
    )
models.signals.post_save.connect(create_profile, sender=User)
