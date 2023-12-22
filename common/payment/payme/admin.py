from django.contrib import admin

from .models import Payment, PaymentVerification

admin.site.register(Payment)
admin.site.register(PaymentVerification)
