from django.db.models.signals import post_save
from django.dispatch import receiver

from api.tasks import createProducts
from common.product.models import File


@receiver(post_save, sender=File)
def fileSave(sender, instance, created, **kwargs):
    createProducts.apply_async([instance.id])
