from pathlib import Path

from .models import AudioResource


def upload_audio_files(files):
    for f in files:
        title = Path(f.name).stem.replace('-', ' ').replace('_', ' ').title()
        AudioResource.objects.create(title=title, file=f, file_size=f.size)
