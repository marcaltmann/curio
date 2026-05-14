from django.db import models
from django.utils.translation import gettext_lazy as _


class AudioResource(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    file = models.FileField(upload_to='audio/', verbose_name=_('file'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('file size'))
    duration = models.DurationField(null=True, blank=True, verbose_name=_('duration'))
    bitrate = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('bitrate'))
    sample_rate = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('sample rate'))
    channels = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('channels'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('audio resource')
        verbose_name_plural = _('audio resources')

    def __str__(self):
        return self.title
