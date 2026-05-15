from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import AudioResource
from .use_cases import upload_audio_files

EMPTY_META = {
    'title': None,
    'duration': None,
    'bitrate': None,
    'sample_rate': None,
    'channels': None,
}


@pytest.mark.django_db
def test_upload_audio_files_creates_resources():
    f = SimpleUploadedFile('my-podcast.mp3', b'audio data')
    upload_audio_files([f])
    assert AudioResource.objects.count() == 1
    resource = AudioResource.objects.first()
    assert resource.title == 'My Podcast'
    assert resource.file_size == len(b'audio data')


@pytest.mark.django_db
def test_upload_audio_files_stores_duration():
    f = SimpleUploadedFile('episode.mp3', b'audio data')
    meta = {**EMPTY_META, 'duration': timedelta(seconds=90)}
    with patch('curio.resources.use_cases.extract_metadata', return_value=meta):
        upload_audio_files([f])
    assert AudioResource.objects.first().duration == timedelta(seconds=90)


@pytest.mark.django_db
def test_upload_audio_files_stores_technical_metadata():
    f = SimpleUploadedFile('episode.mp3', b'audio data')
    meta = {**EMPTY_META, 'bitrate': 128000, 'sample_rate': 44100, 'channels': 2}
    with patch('curio.resources.use_cases.extract_metadata', return_value=meta):
        upload_audio_files([f])
    resource = AudioResource.objects.first()
    assert resource.bitrate == 128000
    assert resource.sample_rate == 44100
    assert resource.channels == 2


@pytest.mark.django_db
def test_upload_audio_files_stores_none_metadata_when_unreadable():
    f = SimpleUploadedFile('episode.mp3', b'not real audio')
    upload_audio_files([f])
    resource = AudioResource.objects.first()
    assert resource.duration is None
    assert resource.bitrate is None
    assert resource.sample_rate is None
    assert resource.channels is None


@pytest.mark.django_db
def test_upload_audio_files_uses_id3_title_when_available():
    f = SimpleUploadedFile('my-podcast.mp3', b'audio data')
    with patch(
        'curio.resources.use_cases.extract_metadata',
        return_value={**EMPTY_META, 'title': 'Custom Tag Title'},
    ):
        upload_audio_files([f])
    assert AudioResource.objects.first().title == 'Custom Tag Title'


@pytest.mark.django_db
def test_upload_audio_files_derives_title_from_filename():
    cases = [
        ('my-podcast.mp3', 'My Podcast'),
        ('another_episode.mp3', 'Another Episode'),
        ('simple.mp3', 'Simple'),
    ]
    for filename, expected_title in cases:
        upload_audio_files([SimpleUploadedFile(filename, b'data')])
    titles = set(AudioResource.objects.values_list('title', flat=True))
    assert titles == {'My Podcast', 'Another Episode', 'Simple'}
