from django.contrib import admin

from .models import AudioResource, ImageResource, VideoResource

admin.site.register(AudioResource)
admin.site.register(ImageResource)
admin.site.register(VideoResource)
