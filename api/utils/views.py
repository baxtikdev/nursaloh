from django.db.models import Prefetch, Count
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from api.paginator import CustomPagination
from api.utils.serializer import CategoryCreateSerializer, SubCategoryCreateSerializer, CategoryListSerializer, \
    CategoryDetailSerializer, SubCategoryListSerializer, SubCategoryDetailSerializer, BrandCreateSerializer, \
    UomCreateSerializer
from common.product.models import Category, SubCategory, Brand, Uom


@extend_schema(tags=["Category"])
class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    lookup_field = 'guid'

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
    lookup_field = 'guid'

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
    lookup_field = 'guid'


@extend_schema(tags=["Uom"])
class UomAPIView(ModelViewSet):
    queryset = Uom.objects.all()
    serializer_class = UomCreateSerializer
    pagination_class = CustomPagination
    lookup_field = 'guid'
