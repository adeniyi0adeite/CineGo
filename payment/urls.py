# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('subscription/', views.subscription, name='subscription'),
    path('subscribe/<int:plan_id>/', views.subscribe_view, name='subscribe_view'),
    path('pay-per-watch/<int:video_id>/', views.pay_per_watch_view, name='pay_per_watch_view'),
    path('callback/', views.paystack_callback, name='paystack_callback'),
    path('active-subscription/', views.active_subscription, name='active_subscription'),
]
