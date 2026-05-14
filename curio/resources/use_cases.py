from datetime import timedelta
from pathlib import Path

import mutagen

from .models import AudioResource


def extract_metadata(file):
    result = {'title': None, 'duration': None, 'bitrate': None, 'sample_rate': None, 'channels': None}
    try:
        audio = mutagen.File(file, easy=True)
    except mutagen.MutagenError:
        return result
    if audio is None:
        return result
    if audio.tags:
        titles = audio.tags.get('title')
        if titles:
            result['title'] = titles[0]
    if audio.info:
        result['duration'] = timedelta(seconds=audio.info.length)
        result['bitrate'] = getattr(audio.info, 'bitrate', None)
        result['sample_rate'] = getattr(audio.info, 'sample_rate', None)
        result['channels'] = getattr(audio.info, 'channels', None)
    return result


def upload_audio_files(files):
    for f in files:
        meta = extract_metadata(f)
        f.seek(0)
        title = meta['title'] or Path(f.name).stem.replace('-', ' ').replace('_', ' ').title()
        AudioResource.objects.create(
            title=title,
            file=f,
            file_size=f.size,
            duration=meta['duration'],
            bitrate=meta['bitrate'],
            sample_rate=meta['sample_rate'],
            channels=meta['channels'],
        )
