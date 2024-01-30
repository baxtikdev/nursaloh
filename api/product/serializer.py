from rest_framework import serializers

from api.utils.serializer import SubCategoryListSerializer, UomCreateSerializer, BrandCreateSerializer, \
    CornerStatusCreateSerializer
from common.product.models import Product, ProductImage
from config.settings.base import env


class ProductImageInListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return env('BASE_URL') + obj.photo_small.url
        return None

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'photo', 'isMain']


class ProductImageInDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return env('BASE_URL') + obj.photo_medium.url
        return None

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'photo', 'isMain']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'description', 'price', 'material',
                  'uom', 'brand', 'size', 'manufacturer', 'quantity', 'discount', 'isTop', 'cornerStatus', 'status']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    images = serializers.SerializerMethodField()
    cornerStatus = CornerStatusCreateSerializer()

    def get_images(self, obj):
        if obj.images:
            return ProductImageInListSerializer(obj.images, many=True).data
        return []

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'price', 'size', 'manufacturer',
                  'quantity', 'discount', 'isTop', 'cornerStatus', 'status', 'images']


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    uom = UomCreateSerializer()
    brand = BrandCreateSerializer()
    images = serializers.SerializerMethodField()
    cornerStatus = CornerStatusCreateSerializer()

    def get_images(self, obj):
        if obj.images:
            return ProductImageInDetailSerializer(obj.images, many=True).data
        return []

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'description', 'price', 'material', 'images',
                  'uom', 'brand', 'size', 'manufacturer', 'quantity', 'discount', 'isTop', 'cornerStatus', 'status']
