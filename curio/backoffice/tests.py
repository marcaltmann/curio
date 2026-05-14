import io
from unittest.mock import patch

import pytest
from django.urls import reverse

from curio.resources.models import AudioResource


@pytest.mark.django_db
def test_dashboard_returns_200(client):
    response = client.get(reverse('backoffice_dashboard'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_audio_list_returns_200(client):
    response = client.get(reverse('backoffice_audio_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_audio_list_shows_resources(client):
    AudioResource.objects.create(title='Test Podcast', file='audio/test.mp3')
    response = client.get(reverse('backoffice_audio_list'))
    assert b'Test Podcast' in response.content


@pytest.mark.django_db
def test_audio_upload_get_returns_200(client):
    response = client.get(reverse('backoffice_audio_upload'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_audio_upload_post_calls_use_case_and_redirects(client):
    f = io.BytesIO(b'audio data')
    f.name = 'my-podcast.mp3'
    with patch('curio.backoffice.views.upload_audio_files') as mock:
        response = client.post(
            reverse('backoffice_audio_upload'),
            {'files': [f]},
            format='multipart',
        )
    assert mock.called
    assert response.status_code == 302
    assert response['Location'] == reverse('backoffice_audio_list')
