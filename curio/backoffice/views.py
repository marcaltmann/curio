from django.shortcuts import redirect, render

from curio.resources.models import AudioResource
from curio.resources.use_cases import upload_audio_files


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


def audio_upload(request):
    if request.method == 'POST':
        upload_audio_files(request.FILES.getlist('files'))
        return redirect('backoffice_audio_list')
    return render(request, 'backoffice/content/audio_upload.html')
