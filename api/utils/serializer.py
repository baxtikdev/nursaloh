from rest_framework import serializers

from common.product.models import Category, SubCategory, Brand, Uom
from config.settings.base import env


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'guid', 'title']


class SubCategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'title']


class SubCategoryWithNumberSerializer(serializers.ModelSerializer):
    subcategoryProductCount = serializers.IntegerField(default=0)

    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'title', 'subcategoryProductCount']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo']


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryWithNumberSerializer(many=True)
    subcategoryCount = serializers.IntegerField(default=0)
    categoryProductCount = serializers.IntegerField(default=0)
    photo_small = serializers.SerializerMethodField()

    def get_photo_small(self, obj):
        if obj.photo:
            return env('BASE_URL') + obj.photo_small.url
        return None

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo_small', 'subcategories', 'subcategoryCount', 'categoryProductCount']


class CategoryDetailSerializer(serializers.ModelSerializer):
    photo_medium = serializers.SerializerMethodField()

    def get_photo_medium(self, banner):
        if banner.photo:
            return env('BASE_URL') + banner.photo_medium.url
        return None

    class Meta:
        model = Category
        fields = ['id', 'guid', 'title', 'photo_medium']


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title']


class SubCategoryListSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer()

    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer()

    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title']


class BrandCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'guid', 'title']


class UomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title']
