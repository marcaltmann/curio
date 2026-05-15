from django.shortcuts import get_object_or_404, redirect, render

from curio.resources.models import AudioResource, ImageResource
from curio.resources.use_cases import upload_audio_files, upload_image_files


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


def audio_detail(request, pk):
    audio = get_object_or_404(AudioResource, pk=pk)
    return render(request, 'backoffice/content/audio_detail.html', {'audio': audio})


def audio_upload(request):
    if request.method == 'POST':
        upload_audio_files(request.FILES.getlist('files'))
        return redirect('backoffice_audio_list')
    return render(request, 'backoffice/content/audio_upload.html')


def image_list(request):
    return render(
        request,
        'backoffice/content/image_list.html',
        {
            'image_list': ImageResource.objects.order_by('-created_at'),
        },
    )


def image_detail(request, pk):
    image = get_object_or_404(ImageResource, pk=pk)
    return render(request, 'backoffice/content/image_detail.html', {'image': image})


def image_upload(request):
    if request.method == 'POST':
        upload_image_files(request.FILES.getlist('files'))
        return redirect('backoffice_image_list')
    return render(request, 'backoffice/content/image_upload.html')
