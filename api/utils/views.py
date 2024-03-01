from django.db.models import Prefetch, Count
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.utils.serializer import CategoryCreateSerializer, SubCategoryCreateSerializer, CategoryListSerializer, \
    CategoryDetailSerializer, SubCategoryListSerializer, SubCategoryDetailSerializer, BrandCreateSerializer, \
    UomCreateSerializer, AddressCreateSerializer, CornerStatusCreateSerializer
from common.product.models import Category, SubCategory, Brand, Uom, CornerStatus
from common.users.models import Address


@extend_schema(tags=["Category"])
class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch(
                lookup="categorySubCategory",
                queryset=SubCategory.objects.annotate(subcategoryProductCount=Count("subcategoryProducts")).all(),
                to_attr='subcategories'
            )
        ).annotate(subcategoryCount=Count("categorySubCategory")). \
            annotate(categoryProductCount=Count("categorySubCategory__subcategoryProducts"))
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = CategoryListSerializer
        return super().list(request, *args)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args)


@extend_schema(tags=["SubCategory"])
class SubCategoryAPIView(ModelViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategoryCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        self.serializer_class = SubCategoryListSerializer
        return super().list(request, *args)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = SubCategoryDetailSerializer
        return super().retrieve(request, *args)


@extend_schema(tags=["Brand"])
class BrandAPIView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


@extend_schema(tags=["Uom"])
class UomAPIView(ModelViewSet):
    queryset = Uom.objects.all()
    serializer_class = UomCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


@extend_schema(tags=["Address"])
class AddressAPIView(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)
        return queryset


@extend_schema(tags=["Corner Status"])
class CornerStatusAPIView(ModelViewSet):
    queryset = CornerStatus.objects.all()
    serializer_class = CornerStatusCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    lookup_field = 'guid'

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset
