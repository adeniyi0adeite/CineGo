# videos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.video_upload, name='video_upload'),
    path('list/', views.video_list, name='video_list'),
    path('categories/', views.video_categories, name='video_categories'),
    path('about/<int:video_id>/', views.video, name='video'),
    path('stream/<int:video_id>/', views.video_stream, name='video_stream'),  # Video streaming URL
]
