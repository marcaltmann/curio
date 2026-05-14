from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='backoffice_dashboard'),
    path('content/audio/', views.audio_list, name='backoffice_audio_list'),
]
