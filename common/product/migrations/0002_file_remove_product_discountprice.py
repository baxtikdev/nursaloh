# Generated by Django 4.1.4 on 2024-01-07 08:55

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("file", models.FileField(upload_to="files")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="product",
            name="discountPrice",
        ),
    ]