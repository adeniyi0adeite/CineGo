# users/urls.py

from django.contrib.auth import logout
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # New URLs for actor and director details
    path('actor/<int:actor_id>/', views.actor_profile, name='actor_profile'),
    path('director/<int:director_id>/', views.director_profile, name='director_profile'),

]
