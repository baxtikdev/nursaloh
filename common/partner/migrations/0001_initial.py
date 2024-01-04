# Generated by Django 4.1.4 on 2024-01-04 10:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("title", models.CharField(blank=True, max_length=250, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("photo", models.ImageField(upload_to="partnerImage", verbose_name="Image")),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="brandPartner",
                        to="product.brand",
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
