from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.product.models import Brand
from common.users.base import BaseModel, BaseMeta


class Partner(BaseModel):
    title = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    photo = models.ImageField(_("Image"), upload_to='partnerImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(1460, 575)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(350, 235)], format='PNG',
                                 options={'quality': 90})
    brand = models.ForeignKey(Brand, related_name="brandPartner", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return self.title
