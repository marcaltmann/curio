from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='backoffice_dashboard'),
    path('content/audio/', views.audio_list, name='backoffice_audio_list'),
    path('content/audio/<int:pk>/', views.audio_detail, name='backoffice_audio_detail'),
    path('content/audio/upload/', views.audio_upload, name='backoffice_audio_upload'),
]
