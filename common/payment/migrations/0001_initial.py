# Generated by Django 4.1.4 on 2024-01-30 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0003_alter_orderproduct_orderprice"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("amount", models.FloatField(default=0, null=True)),
                ("paymentType", models.IntegerField(choices=[(1, "PAYME"), (2, "CLICK"), (3, "UZUM"), (4, "CASH")])),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "WAITING"),
                            ("preauth", "PREAUTH"),
                            ("confirmed", "CONFIRMED"),
                            ("rejected", "REJECTED"),
                            ("refunded", "REFUNDED"),
                            ("error", "ERROR"),
                        ],
                        default="waiting",
                        max_length=20,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orderPayment",
                        to="order.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userPayment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PaymentVerification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("token", models.CharField(max_length=500)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="paymentVerify", to="payment.payment"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
