from rest_framework import serializers

from api.utils.serializer import SubCategoryListSerializer, UomCreateSerializer, BrandCreateSerializer
from common.product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    model = Product
    fields = ['id', 'guid', 'subcategory', 'code', 'title', 'description', 'price', 'discountPrice', 'material', 'uom',
              'brand', 'size', 'manufacturer', 'quantity', 'discount', 'isTop', 'cornerStatus', 'status']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()

    model = Product
    fields = ['id', 'guid', 'subcategory', 'code', 'title', 'price', 'discountPrice', 'size', 'manufacturer',
              'quantity', 'discount', 'isTop', 'cornerStatus', 'status']


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    uom = UomCreateSerializer()
    brand = BrandCreateSerializer()

    model = Product
    fields = ['id', 'guid', 'subcategory', 'code', 'title', 'description', 'price', 'discountPrice', 'material', 'uom',
              'brand', 'size', 'manufacturer', 'quantity', 'discount', 'isTop', 'cornerStatus', 'status']
