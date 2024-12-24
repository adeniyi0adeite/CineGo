from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, SubscriptionPlan, SubscriptionPayment, VideoAccessPayment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'status', 'payment_type', 'created_at', 'verify_payment_action')
    list_editable = ('status', 'payment_type')
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = ('user__user__username', 'reference', 'status', 'payment_type')
    ordering = ('-created_at',)
    readonly_fields = ('reference', 'created_at')

    def verify_payment_action(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="/admin/payment/verify/{0}/">Verify</a>',
                obj.reference
            )
        return 'N/A'
    verify_payment_action.short_description = 'Verify Payment'

admin.site.register(Payment, PaymentAdmin)
admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionPayment)
admin.site.register(VideoAccessPayment)
