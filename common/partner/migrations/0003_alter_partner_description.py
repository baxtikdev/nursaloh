# Generated by Django 4.1.4 on 2024-01-04 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("partner", "0002_alter_partner_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
