from django.contrib import admin
from .models import UserProfile
from payment.models import SubscriptionPayment

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_fullname', 'get_active_subscription', 'bio')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('user__is_active',)

    def get_fullname(self, obj):
        """Get the full name of the user."""
        return obj.get_fullname()
    get_fullname.short_description = 'Full Name'

    def get_active_subscription(self, obj):
        """Display the active subscription if it exists."""
        active_subscription = obj.get_active_subscription()
        if active_subscription:
            return f"{active_subscription.plan.name} (Expires: {active_subscription.end_date})"
        return "No Active Subscription"
    get_active_subscription.short_description = 'Active Subscription'

admin.site.register(UserProfile, UserProfileAdmin)
