from django.db.models import Prefetch, Q
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import ProductFilter
from api.paginator import CustomPagination
from api.product.serializer import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer
from common.product.models import Product, ProductImage


@extend_schema(tags=["Product"])
class ProductAPIView(ModelViewSet):
    queryset = Product.objects.select_related('subcategory', 'subcategory__category', 'brand', 'uom').all()
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [ProductFilter, OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(subcategory__category_id__in=category.split(','))

        subcategory = self.request.query_params.get('subcategory')
        if subcategory:
            queryset = queryset.filter(subcategory_id__in=subcategory.split(','))

        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__id__in=brand.split(','))

        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(id__in=id.split(','))

        startPrice = self.request.query_params.get('startPrice')
        if startPrice and startPrice.isdigit():
            queryset = queryset.filter(price__gte=startPrice)

        toPrice = self.request.query_params.get('toPrice')
        if toPrice and toPrice.isdigit():
            queryset = queryset.filter(price__lte=toPrice)

        filters = {}
        fields = ['uom', 'cornerStatus']

        for field in fields:
            param_value = self.request.query_params.get(field)
            if param_value:
                filters[f'{field}__exact'] = param_value

        if self.request.query_params.get('isTop'):
            filters['isTop'] = True

        if self.request.query_params.get('status'):
            filters['status'] = self.request.query_params.get('status')

        queryset = queryset.filter(**filters)

        q = self.request.query_params.get('q')
        if q:
            q_objects = Q()
            fields = ['code', 'title', 'description', 'price', 'material', 'brand__title',
                      'manufacturer']
            for field in fields:
                q_objects |= Q(**{f'{field}__icontains': q})

            queryset = queryset.filter(q_objects)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().prefetch_related(
            Prefetch(
                lookup="productProductImage",
                queryset=ProductImage.objects.all(),  # .filter(isMain=True).all(),
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
