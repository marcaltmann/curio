from django.shortcuts import render

from curio.resources.models import AudioResource


def dashboard(request):
    return render(request, 'backoffice/dashboard.html')


def audio_list(request):
    return render(
        request,
        'backoffice/content/audio_list.html',
        {
            'audio_list': AudioResource.objects.order_by('-created_at'),
        },
    )
