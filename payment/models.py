# payment/models.py


from django.db import models
from django.utils import timezone
from users.models import UserProfile
from videos.models import Video, VideoAccess
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
import requests
import uuid

# Constants for subscription plans
PLAN_CHOICES = [
    ('Basic', 'Basic'),
    ('Premium', 'Premium'),
    ('Vip', 'VIP'),
]

SUPPORT_CHOICES = [
    ('Limited Support', 'Limited Support'),
    ('24/7 Support', '24/7 Support'),
]

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1000.00)
    duration = models.IntegerField(default=30, help_text="Duration of the plan in days")
    resolution = models.CharField(max_length=50, choices=[('HD', 'HD'), ('Full HD', 'Full HD'), ('4K', '4K')], default='HD')
    device = models.CharField(max_length=100, blank=True, null=True)
    support = models.CharField(max_length=20, choices=SUPPORT_CHOICES, default='Limited Support')

    def __str__(self):
        return f"{self.get_name_display()} - {self.price} NGN"


class SubscriptionPayment(models.Model):
    user = models.ForeignKey(UserProfile, related_name='subscriptions', on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)  # Link SubscriptionPlan here
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.user.username} - {self.plan.name.capitalize()} - {self.plan.price} NGN"

    def save(self, *args, **kwargs):
        """Override save to calculate end_date based on plan duration."""
        if not self.plan:
            raise ValidationError("Subscription plan is required.")
        
        # Set end date based on the plan's duration
        self.end_date = self.start_date + timedelta(days=self.plan.duration)
        super().save(*args, **kwargs)

    def is_active(self):
        """Check if the subscription is currently active."""
        return timezone.now() <= self.end_date


class VideoAccessPayment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('successful', 'Successful')], default='pending')
    date_paid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user.username} - {self.video.title} - {self.status}"


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('subscription', 'Subscription'),
        ('pay_per_watch', 'Pay Per Watch'),
    ]

    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.payment_type.capitalize()} - {self.amount} NGN"

    def process_payment(self):
        """Process the payment using Paystack API."""
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": self.user.user.email,
            "amount": int(self.amount * 100),  # Paystack accepts amounts in kobo
            "reference": self.reference,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get("status"):
            return result['data']['authorization_url']
        else:
            raise Exception("Payment initialization failed. Please try again.")

    def verify_payment(self):
        """Verify the payment using Paystack API and update status."""
        url = f"https://api.paystack.co/transaction/verify/{self.reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        response = requests.get(url, headers=headers)
        result = response.json()

        if result.get("status"):
            self.status = 'completed' if result['data']['status'] == 'success' else 'failed'
            self.save()
            if self.status == 'completed':
                self.handle_successful_payment()
        else:
            self.status = 'failed'
            self.save()

    def handle_successful_payment(self):
        """Handle post-payment processing based on payment type."""
        if self.payment_type == 'subscription':
            self.handle_subscription_payment()
        elif self.payment_type == 'pay_per_watch':
            self.handle_pay_per_watch_payment()

    def handle_subscription_payment(self):
        """Handle subscription payment after verification."""
        subscription = SubscriptionPayment.objects.filter(user=self.user, plan=self.plan).first()
        if not subscription:
            raise ValidationError("No matching subscription plan found.")
        
        subscription.start_date = timezone.now()
        subscription.end_date = subscription.start_date + timedelta(days=subscription.plan.duration)
        subscription.save()

    def handle_pay_per_watch_payment(self):
        """Handle pay-per-watch payment after verification."""
        # Find the corresponding video payment object
        video_payment = VideoAccessPayment.objects.filter(user=self.user, transaction_reference=self.reference).first()
        
        if not video_payment:
            raise ValidationError("No matching video access payment found.")
        
        # Create a new VideoAccess entry to grant the user access to the video
        VideoAccess.objects.create(user=self.user, video=video_payment.video)
        
        # Update the video payment status to 'successful'
        video_payment.status = 'successful'
        video_payment.save()

