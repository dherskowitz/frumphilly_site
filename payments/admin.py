from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("ad_uuid", "email", "payment_status", "purchase_type", "purchase_choice")
    list_filter = ("payment_status", "purchase_type", "purchase_choice")


admin.site.register(Payment, PaymentAdmin)
