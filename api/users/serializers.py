from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from api.utils.serializer import AddressCreateSerializer
from config.settings.base import env

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo']


class UserUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo']


class UserListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo_small.url
        return None

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo']


class UserDetailSerializer(serializers.ModelSerializer):
    userAddress = AddressCreateSerializer(many=True)
    photo = serializers.SerializerMethodField()

    def get_photo(self, product):
        if product.photo:
            return env('BASE_URL') + product.photo_medium.url
        return None

    class Meta:
        model = User
        fields = ['id', 'guid', 'name', 'phone', 'photo', 'userAddress']
