from django.contrib.auth import get_user_model
from django.db import models
from common.users.base import BaseModel

User = get_user_model()


class PaymentStatus(models.TextChoices):
    WAITING = "waiting", "WAITING"
    PREAUTH = "preauth", "PREAUTH"
    CONFIRMED = "confirmed", "CONFIRMED"
    REJECTED = "rejected", "REJECTED"
    REFUNDED = "refunded", "REFUNDED"
    ERROR = "error", "ERROR"


class PaymentType(models.IntegerChoices):
    PAYME = 1, "PAYME"
    CLICK = 2, "CLICK"
    UZUM = 3, "UZUM"


class Payment(BaseModel):
    user = models.ForeignKey(User, related_name="userPayment", on_delete=models.CASCADE)
    order = models.ForeignKey("order.Order", related_name="orderPayment", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(default=0, null=True)
    paymentType = models.IntegerField(choices=PaymentType.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.WAITING)

    def __str__(self):
        return f"{self.user.name} | {self.amount} | {self.paymentType}"


class PaymentVerification(BaseModel):
    payment = models.ForeignKey(Payment, related_name="paymentVerify", on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.time}"
