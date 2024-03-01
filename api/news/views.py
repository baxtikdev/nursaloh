from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.news.serializers import NewsListSerializer, NewsCreateSerializer, NewsDetailSerializer
from api.paginator import CustomPagination
from api.permissions import IsAdmin
from common.news.models import News


@extend_schema(tags=["News"])
class NewsAPIView(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = CustomPagination
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        isActual = self.request.query_params.get('isActual')
        if isActual == 'true':
            queryset = queryset.filter(isActual=True)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = NewsListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = NewsDetailSerializer
        return super().retrieve(request, *args, **kwargs)
