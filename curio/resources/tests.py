from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import AudioResource
from .use_cases import upload_audio_files


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
    with patch('curio.resources.use_cases.extract_duration', return_value=timedelta(seconds=90)):
        upload_audio_files([f])
    assert AudioResource.objects.first().duration == timedelta(seconds=90)


@pytest.mark.django_db
def test_upload_audio_files_stores_none_duration_when_unreadable():
    f = SimpleUploadedFile('episode.mp3', b'not real audio')
    upload_audio_files([f])
    assert AudioResource.objects.first().duration is None


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
