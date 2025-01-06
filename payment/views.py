from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Payment
from django.db import transaction

from videos.models import Video, VideoAccess
from .models import SubscriptionPlan, Video, Payment, SubscriptionPayment, VideoAccessPayment

import uuid

@login_required
def payment_page(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'payment/payment_page.html', {'video': video})

@login_required
def subscription(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'payment/subscription.html', {'plans': plans})



@login_required
def active_subscription(request):
    active_sub = request.user.userprofile.get_active_subscription()  # Corrected method call
    
    if active_sub:
        videos = []
    else:
        video_access = VideoAccess.objects.filter(user=request.user.userprofile).select_related('video')
        videos = [access.video for access in video_access]
    
    return render(request, 'payment/active_subscription.html', {
        'active_subscription': active_sub,
        'videos': videos,
        'message': "You have an active subscription" if active_sub else "You have no active subscription."
    })



@login_required
def subscribe_view(request, plan_id):
    """Handle subscription purchase process."""
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

    # Create a payment object to initialize the payment
    payment = Payment.objects.create(
        user=request.user.userprofile,
        amount=plan.price,
        reference=str(uuid.uuid4()),
        payment_type='subscription',
        status='pending'
    )

    # Initialize the payment with Paystack
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": request.user.email,
        "amount": int(plan.price * 100),  # Paystack accepts amounts in kobo
        "reference": payment.reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    if result.get("status"):
        payment.status = 'completed'
        payment.save()
        return JsonResponse({"success": True, "authorization_url": result['data']['authorization_url']})
    else:
        return JsonResponse({"success": False, "error": result.get('message', 'Error occurred while initializing payment')})




@login_required
def pay_per_watch_view(request, video_id):
    """Handle pay-per-watch payments after free watch time."""
    video = get_object_or_404(Video, pk=video_id)

    # Assume price is set in the video model
    payment = Payment.objects.create(
        user=request.user.userprofile,
        amount=video.price,
        reference=str(uuid.uuid4()),
        payment_type='pay_per_watch',
        status='pending'
    )

    # Initialize the payment with Paystack
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": request.user.email,
        "amount": int(video.price * 100),  # Convert price to kobo
        "reference": payment.reference,
        "callback_url": f"{settings.PAYSTACK_CALLBACK_URL}?video_id={video.id}",
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    if result.get("status"):
        # Redirect the user to Paystack's authorization URL
        return redirect(result['data']['authorization_url'])
    else:
        # Handle error (you may want to display a message or log it)
        return HttpResponse("Error occurred while initializing payment", status=400)


@login_required
def paystack_callback(request):
    """Handle Paystack's callback after payment is completed."""
    reference = request.GET.get('reference')
    video_id = request.GET.get('video_id')  # Get video_id from the callback URL
    
    print(f"Callback received: reference={reference}, video_id={video_id}")  # Add debug print
    
    if reference:
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        
        print(f"Paystack verify response: {result}")  # Add debug print
        
        if result.get("status") and result['data']['status'] == 'success':
            payment = Payment.objects.get(reference=reference)
            payment.status = 'completed'
            payment.save()

            # Handle subscription payments
            if payment.payment_type == 'subscription':
                plan = SubscriptionPlan.objects.get(price=payment.amount)
                SubscriptionPayment.objects.create(
                    user=payment.user,
                    plan=plan,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=plan.duration)
                )
                return redirect('active_subscription')  # Redirect to active subscription page

            # Handle pay-per-watch payments
            if payment.payment_type == 'pay_per_watch':
                # Ensure the video payment is marked successful
                video_access_payment = VideoAccessPayment.objects.create(
                    user=payment.user,
                    video=Video.objects.get(id=video_id),
                    amount=payment.amount,
                    transaction_reference=payment.reference,
                    status='successful'
                )
                
                # Automatically grant video access to the user
                VideoAccess.objects.create(
                    user=payment.user,
                    video=video_access_payment.video
                )
                
                return redirect('video_stream', video_id=video_id)  # Redirect to the video stream page


    return redirect('active_subscription')  # Fallback to active subscription if anything goes wrong
