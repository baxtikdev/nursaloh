from django.urls import path

from .views import PaymentClick, PaymentPrepareAPIView, PaymentCompleteAPIView

urlpatterns = [
    path('-prepare/', PaymentPrepareAPIView.as_view(), name='click_prepare'),
    path('-complete/', PaymentCompleteAPIView.as_view(), name='click_complete'),
    path('-pay/', PaymentClick.as_view(), name='click_payment')
]
