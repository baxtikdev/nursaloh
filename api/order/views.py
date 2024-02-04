from django.db.models import Prefetch, Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.exceptions import ProductNotFoundException
from api.filters import OrderFilter
from api.order.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer, \
    OrderProductCreateSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient, IsAdmin
from common.order.models import Order, OrderProduct, OrderStatus
from common.payment.models import PaymentType
from common.product.models import Product


@extend_schema(tags=["Order"])
class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    filter_backends = [OrderFilter, OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = CustomPagination
    permission_classes = [IsClient | IsAdmin]
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user', 'address'). \
            prefetch_related(
            Prefetch(
                lookup="products",
                queryset=OrderProduct.objects.select_related('product', 'product__uom', 'product__brand',
                                                             'product__cornerStatus').all(),
                # to_attr="orderProducts"
            )
        ).annotate(orderCount=Count('products'))

        return queryset

    def create(self, request, *args, **kwargs):
        orderProducts = request.data.get('orderProducts', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # orderProducts = [
        #     {
        #         "product": 1,
        #         "quantity": 4,
        #     }
        # ]
        if not orderProducts:
            return Response({"orderProducts": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        orderedProducts = []
        totalAmount = 0
        for orderProduct in orderProducts:
            product = orderProduct.get('product')
            quantity = orderProduct.get('quantity')
            product = Product.objects.filter(id=product).first()
            if product is None:
                raise ProductNotFoundException()
            orderProduct['orderPrice'] = round(product.with_discount, 3)
            orderProduct['discount'] = round(product.discount, 3)

            orderProduct_serializer = OrderProductCreateSerializer(data=orderProduct)
            orderProduct_serializer.is_valid(raise_exception=True)
            orderedProducts.append(**orderProduct_serializer.validated_data)
            totalAmount += round(product.with_discount * quantity, 3)
        if orderedProducts:
            OrderProduct.objects.bulk_create(orderProducts)

        order = serializer.save()
        if order.paymentType == PaymentType.CASH:
            order.status = OrderStatus.PENDING
        order.products.set(orderProducts)
        order.totalAmount = totalAmount
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        self.serializer_class = OrderListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = OrderDetailSerializer
        return super().retrieve(request, *args, **kwargs)
