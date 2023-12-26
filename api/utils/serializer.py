from rest_framework import serializers

from common.product.models import Category, SubCategory, Brand, Uom
from config.settings.base import env


class CategoryShortSerializer(serializers.ModelSerializer):
    model = Category
    fields = ['id', 'guid', 'title']


class SubCategoryShortSerializer(serializers.ModelSerializer):
    model = SubCategory
    fields = ['id', 'guid', 'title']


class SubCategoryWithNumberSerializer(serializers.ModelSerializer):
    categoryProductCount = serializers.IntegerField(default=0)

    model = SubCategory
    fields = ['id', 'guid', 'title']


class CategoryCreateSerializer(serializers.ModelSerializer):
    model = Category
    fields = ['id', 'guid', 'title', 'photo']


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryWithNumberSerializer(many=True)
    subcategoryProductCount = serializers.IntegerField(default=0)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, banner):
        if banner.photo:
            return env('BASE_URL') + banner.photo_small.url
        return None

    model = Category
    fields = ['id', 'guid', 'title', 'photo_small', 'subcategories']


class CategoryDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, banner):
        if banner.photo:
            return env('BASE_URL') + banner.photo_medium.url
        return None

    model = Category
    fields = ['id', 'guid', 'title', 'photo_medium']


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    model = SubCategory
    fields = ['id', 'guid', 'category', 'title']


class SubCategoryListSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer()

    model = SubCategory
    fields = ['id', 'guid', 'category', 'title']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer()

    model = SubCategory
    fields = ['id', 'guid', 'category', 'title']


class BrandCreateSerializer(serializers.ModelSerializer):
    model = Brand
    fields = ['id', 'guid', 'title']


class UomCreateSerializer(serializers.ModelSerializer):
    model = Uom
    fields = ['id', 'guid', 'title']
