from django.db.models import Prefetch
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import ProductFilter
from api.paginator import CustomPagination
from api.product.serializer import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer
from common.product.models import Product, ProductImage


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.select_related('subcategory', 'subcategory__category', 'brand', 'uom').all()
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [ProductFilter, OrderingFilter]
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().prefetch_related(
            Prefetch(
                lookup="productProductImage",
                queryset=ProductImage.objects.filter(isMain=True).all(),
                to_attr="images"
            )
        )
        self.serializer_class = ProductListSerializer

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance = self.get_queryset().prefetch_related(
            Prefetch(
                lookup="productProductImage",
                queryset=ProductImage.objects.all(),
                to_attr="images"
            )
        ).filter(id=instance.id).first()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)
