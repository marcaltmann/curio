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
