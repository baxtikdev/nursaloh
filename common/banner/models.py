from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta


class Banner(BaseModel):
    photo_uz = models.ImageField(_("Image of Banner"), upload_to='bannerImage', null=True, blank=True)
    photo_medium_uz = ImageSpecField(source='photo_uz', processors=[ResizeToFill(1463, 420)], format='PNG',
                                     options={'quality': 100})
    photo_small_uz = ImageSpecField(source='photo_uz', processors=[ResizeToFill(322, 209)], format='PNG',
                                    options={'quality': 70})
    photo_ru = models.ImageField(_("Image of Banner"), upload_to='bannerImage', null=True, blank=True)
    photo_medium_ru = ImageSpecField(source='photo_ru', processors=[ResizeToFill(1463, 420)], format='PNG',
                                     options={'quality': 100})
    photo_small_ru = ImageSpecField(source='photo_ru', processors=[ResizeToFill(322, 209)], format='PNG',
                                    options={'quality': 70})
    url = models.CharField(max_length=250, null=True, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return f"Banner #{self.id}"
