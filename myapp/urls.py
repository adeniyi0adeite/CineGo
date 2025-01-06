# myapp/urls.py
from django.urls import path
from . import views


# Custom 404 handler
handler404 = 'myapp.views.custom_page_not_found_view'


urlpatterns = [
    path('', views.home_view, name='home'),
]

