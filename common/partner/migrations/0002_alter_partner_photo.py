# Generated by Django 4.2.5 on 2023-12-22 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("partner", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="photo",
            field=models.ImageField(upload_to="partnerImage", verbose_name="Image"),
        ),
    ]
