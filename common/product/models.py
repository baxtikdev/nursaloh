from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta

User = get_user_model()


class ProductStatus(models.IntegerChoices):
    DRAFT = 1, "DRAFT"
    ACTIVE = 2, "ACTIVE"
    DELETED = 3, "DELETED"


class CornerStatus(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    # NEWS = 1, "NEWS"
    # DISCOUNT = 2, "DISCOUNT"
    # SPECIAL = 3, "SPECIAL"
    # RECOMMENDATION = 4, "RECOMMENDATION"
    # CHEAP = 5, "CHEAP"
    # EXPENSIVE = 6, "EXPENSIVE"
    # POPULAR = 7, "POPULAR"


class Uom(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Brand(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=255)
    photo = models.ImageField(_("Image of Category"), upload_to='categoryImage', null=True, blank=True)
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(200, 200)], format='PNG',
                                 options={'quality': 90})
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(500, 500)], format='PNG',
                                  options={'quality': 90})

    def __str__(self):
        return self.title


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, related_name="categorySubCategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(BaseModel):
    subcategory = models.ForeignKey(SubCategory, related_name="subcategoryProducts", on_delete=models.SET_NULL,
                                    null=True, blank=True)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    price = models.FloatField(default=0)
    discountPrice = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name="uomProduct", on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name="brandProduct", on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    manufacturer = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    isTop = models.BooleanField(_("Is Top"), default=False)
    cornerStatus = models.ForeignKey(CornerStatus, related_name="cornerStatusProduct", on_delete=models.SET_NULL,
                                     null=True, blank=True)
    status = models.IntegerField(choices=ProductStatus.choices, default=ProductStatus.DRAFT)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='productProductImage', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='productImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(500, 500)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(200, 200)], format='PNG',
                                 options={'quality': 90})
    isMain = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
