from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='backoffice_dashboard'),
    path('content/audio/', views.audio_list, name='backoffice_audio_list'),
    path('content/audio/<int:pk>/', views.audio_detail, name='backoffice_audio_detail'),
    path('content/audio/upload/', views.audio_upload, name='backoffice_audio_upload'),
    path('content/images/', views.image_list, name='backoffice_image_list'),
    path(
        'content/images/<int:pk>/', views.image_detail, name='backoffice_image_detail'
    ),
    path('content/images/upload/', views.image_upload, name='backoffice_image_upload'),
    path('content/videos/', views.video_list, name='backoffice_video_list'),
    path(
        'content/videos/<int:pk>/', views.video_detail, name='backoffice_video_detail'
    ),
    path('content/videos/upload/', views.video_upload, name='backoffice_video_upload'),
]
