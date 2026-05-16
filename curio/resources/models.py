from django.db import models
from django.utils.translation import gettext_lazy as _


class AudioResource(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    file = models.FileField(upload_to='audio/', verbose_name=_('file'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('file size'))
    duration = models.DurationField(null=True, blank=True, verbose_name=_('duration'))
    bitrate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('bitrate')
    )
    sample_rate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('sample rate')
    )
    channels = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name=_('channels')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('audio resource')
        verbose_name_plural = _('audio resources')

    def __str__(self):
        return self.title


class ImageResource(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    file = models.ImageField(upload_to='images/', verbose_name=_('file'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('file size'))
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('width'))
    height = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('height')
    )
    format = models.CharField(
        max_length=32, null=True, blank=True, verbose_name=_('format')
    )
    color_mode = models.CharField(
        max_length=16, null=True, blank=True, verbose_name=_('color mode')
    )
    icc_profile = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('ICC profile')
    )
    taken_at = models.DateTimeField(null=True, blank=True, verbose_name=_('taken at'))
    camera_make = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('camera make')
    )
    camera_model = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('camera model')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('image resource')
        verbose_name_plural = _('image resources')

    def __str__(self):
        return self.title


class VideoResource(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    file = models.FileField(upload_to='videos/', verbose_name=_('file'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('file size'))
    poster = models.ImageField(
        upload_to='video_posters/', null=True, blank=True, verbose_name=_('poster')
    )
    duration = models.DurationField(null=True, blank=True, verbose_name=_('duration'))
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('width'))
    height = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('height')
    )
    bitrate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('bitrate')
    )
    video_codec = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('video codec')
    )
    frame_rate_num = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('frame rate numerator')
    )
    frame_rate_den = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('frame rate denominator')
    )
    audio_codec = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('audio codec')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('video resource')
        verbose_name_plural = _('video resources')

    def __str__(self):
        return self.title
