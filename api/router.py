from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.order.views import OrderAPIView
from api.product.views import ProductAPIView
from api.utils.views import CategoryAPIView, SubCategoryAPIView, BrandAPIView, UomAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# app_name = "api"
router.register(r"product", ProductAPIView, basename='product')
router.register(r"category", CategoryAPIView, basename='category')
router.register(r"subcategory", SubCategoryAPIView, basename='subcategory')
router.register(r"brand", BrandAPIView, basename='brand')
router.register(r"uom", UomAPIView, basename='uom')
router.register(r"order", OrderAPIView, basename='order')

urlpatterns = router.urls
