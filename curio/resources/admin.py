from django.contrib import admin

from .models import AudioResource, ImageResource, Metadata, Resource, VideoResource


class MetadataInline(admin.TabularInline):
    model = Metadata
    extra = 0


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    inlines = [MetadataInline]


admin.site.register(AudioResource)
admin.site.register(ImageResource)
admin.site.register(VideoResource)
