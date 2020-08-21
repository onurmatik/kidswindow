from django.db import models
from django.utils.translation import ugettext_lazy as _


class Game(models.Model):
    name = models.CharField(_('name'), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('game')
        verbose_name_plural = _('games')
