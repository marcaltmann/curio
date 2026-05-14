from datetime import timedelta
from pathlib import Path

import mutagen

from .models import AudioResource


def extract_duration(file):
    try:
        audio = mutagen.File(file)
    except mutagen.MutagenError:
        return None
    if audio is None or audio.info is None:
        return None
    return timedelta(seconds=audio.info.length)


def upload_audio_files(files):
    for f in files:
        title = Path(f.name).stem.replace('-', ' ').replace('_', ' ').title()
        duration = extract_duration(f)
        f.seek(0)
        AudioResource.objects.create(title=title, file=f, file_size=f.size, duration=duration)
