from rest_framework import serializers

from api.product.serializer import ProductDetailSerializer
from common.order.models import Order, OrderProduct
from common.users.models import User


class OrderProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'discount']


class OrderProductListSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'orderPrice', 'discount']


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    installation = serializers.BooleanField()
    paymentType = serializers.IntegerField()
    billing_url = serializers.CharField(allow_null=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'address', 'installation', 'comment', 'paymentType', 'billing_url']


class OrderListSerializer(serializers.ModelSerializer):
    products = OrderProductListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'code', 'products', 'totalAmount', 'orderedTime', 'deliveredTime', 'comment',
                  'paymentStatus', 'paymentType', 'status']


class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'products', 'address', 'totalAmount', 'orderedTime', 'deliveredTime',
                  'installation', 'comment', 'installation', 'paymentStatus', 'paymentType', 'status']
