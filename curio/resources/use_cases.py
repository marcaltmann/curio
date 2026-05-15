import io
from datetime import datetime, timedelta
from pathlib import Path

import mutagen
from PIL import Image, ImageCms

from .models import AudioResource, ImageResource


def extract_metadata(file):
    result = {
        'title': None,
        'duration': None,
        'bitrate': None,
        'sample_rate': None,
        'channels': None,
    }
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


_EXIF_TAG_MAKE = 271
_EXIF_TAG_MODEL = 272
_EXIF_TAG_DATETIME_ORIGINAL = 36867


def extract_image_metadata(file):
    result = {
        'width': None,
        'height': None,
        'format': None,
        'color_mode': None,
        'icc_profile': None,
        'taken_at': None,
        'camera_make': None,
        'camera_model': None,
    }
    try:
        img = Image.open(file)
        img.load()
    except Exception:
        return result
    result['width'], result['height'] = img.size
    result['format'] = img.format
    result['color_mode'] = img.mode
    icc_data = img.info.get('icc_profile')
    if icc_data:
        try:
            profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_data))
            result['icc_profile'] = ImageCms.getProfileName(profile).strip()
        except Exception:
            pass
    try:
        exif = img.getexif()
        taken_str = exif.get(_EXIF_TAG_DATETIME_ORIGINAL)
        if taken_str:
            from django.utils import timezone

            naive = datetime.strptime(taken_str, '%Y:%m:%d %H:%M:%S')
            result['taken_at'] = timezone.make_aware(naive)
        result['camera_make'] = exif.get(_EXIF_TAG_MAKE) or None
        result['camera_model'] = exif.get(_EXIF_TAG_MODEL) or None
    except Exception:
        pass
    return result


def upload_image_files(files):
    for f in files:
        meta = extract_image_metadata(f)
        f.seek(0)
        title = Path(f.name).stem.replace('-', ' ').replace('_', ' ').title()
        ImageResource.objects.create(
            title=title,
            file=f,
            file_size=f.size,
            **meta,
        )


def upload_audio_files(files):
    for f in files:
        meta = extract_metadata(f)
        f.seek(0)
        title = (
            meta['title']
            or Path(f.name).stem.replace('-', ' ').replace('_', ' ').title()
        )
        AudioResource.objects.create(
            title=title,
            file=f,
            file_size=f.size,
            duration=meta['duration'],
            bitrate=meta['bitrate'],
            sample_rate=meta['sample_rate'],
            channels=meta['channels'],
        )
