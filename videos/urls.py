# videos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.video_upload, name='video_upload'),  # Video upload URL
    path('all/', views.video_list, name='video_list'),  # List all videos URL
]
