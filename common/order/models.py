from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.payment.models import PaymentStatus, PaymentType
from common.product.models import Product
from common.users.base import BaseModel, BaseMeta
from common.users.models import Address

User = get_user_model()


class OrderStatus(models.IntegerChoices):
    PAYMENT = 0, "PAYMENT"
    PENDING = 1, "PENDING"
    WAITING = 2, "WAITING"
    DELIVERED = 3, "DELIVERED"
    CANCELED = 4, "CANCELED"
    IN_PROGRESS = 5, "IN_PROGRESS"
    DELETED = 6, "DELETED"


class OrderProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    orderPrice = models.DecimalField(max_digits=50, decimal_places=3, default=0)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f"Order Product #{self.id} {self.product.title} {self.quantity}"


class Order(BaseModel):
    user = models.ForeignKey(User, related_name="orderUser", on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, editable=False)
    address = models.ForeignKey(Address, related_name="orderAddress", on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderProduct, related_name='orderedProducts', blank=True)
    totalAmount = models.FloatField(default=0)
    orderedTime = models.DateTimeField(default=timezone.now)
    deliveredTime = models.DateTimeField(null=True, blank=True)
    installation = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)

    paymentStatus = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.WAITING)
    paymentType = models.IntegerField(choices=PaymentType.choices, default=PaymentType.CASH)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PAYMENT)

    class Meta(BaseMeta):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.code is None:
            self.code = 'P' + str(self.id + (10 ** 4))
            self.save()

    def __str__(self):
        return f"Order #{self.id} Status: {self.status} Payment Status: {self.paymentStatus}"
