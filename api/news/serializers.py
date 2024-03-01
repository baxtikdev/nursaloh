from rest_framework import serializers

from common.news.models import News
from config.settings.base import env


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'middle_description', 'description', 'videoURL', 'viewCount', 'status',
                  'isActual']


class NewsListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return env('BASE_URL') + obj.photo_small.url
        return None

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'middle_description', 'videoURL', 'viewCount', 'status', 'isActual']


class NewsDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return env('BASE_URL') + obj.photo_medium.url
        return None

    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'middle_description', 'description', 'videoURL', 'viewCount', 'status',
                  'isActual']
