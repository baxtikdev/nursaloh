from rest_framework import serializers

from common.news.models import News


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'middle_description', 'description', 'videoURL', 'viewCount', 'status',
                  'isActual']


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'guid', 'title', 'middle_description', 'videoURL', 'viewCount', 'status', 'isActual']
