from django.db.models import Q
from rest_framework import filters

from common.order.models import PaymentTypes, PaymentStatus
from common.users.models import User


class ProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}
        fields = ['subcategory', 'uom', 'brand', 'cornerStatus']

        for field in fields:
            param_value = request.query_params.get(field)
            if param_value:
                filters[f'{field}__exact'] = param_value
        category = request.query_params.get('category')
        if category:
            filters['subcategory__category__id__in'] = category.split(',')

        subcategory = request.query_params.get('subcategory')
        if subcategory:
            filters['subcategory__id__in'] = subcategory.split(',')

        brand = request.query_params.get('brand')
        if brand:
            filters['brand__id__in'] = brand.split(',')

        id = request.query_params.get('id')
        if id:
            filters['id__in'] = id.split(',')

        startPrice = request.query_params.get('startPrice')
        if startPrice:
            filters['startPrice__gte'] = startPrice

        toPrice = request.query_params.get('toPrice')
        if toPrice:
            filters['toPrice__lte'] = toPrice

        if request.query_params.get('isTop'):
            filters['isTop'] = True

        if request.query_params.get('status'):
            filters['status'] = request.query_params.get('status')

        queryset = queryset.filter(**filters)
        q = request.query_params.get('q')
        if q:
            q_objects = Q()
            fields = ['code', 'title', 'description', 'price', 'discountPrice', 'material', 'brand__title',
                      'manufacturer']
            for field in fields:
                q_objects |= Q(**{f'{field}__icontains': q})

            queryset = queryset.filter(q_objects)

        return queryset


class OrderFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}
        fields = ['user', 'address']

        for field in fields:
            param_value = request.query_params.get(field)
            if param_value:
                filters[f'{field}__exact'] = param_value

        if request.query_params.get('installation'):
            filters['installation'] = True

        if request.query_params.get('paymentStatus'):
            filters['paymentStatus'] = request.query_params.get('paymentStatus')

        if request.query_params.get('paymentType'):
            filters['paymentType'] = request.query_params.get('paymentType')

        if request.query_params.get('status'):
            filters['status'] = request.query_params.get('status')

        queryset = queryset.filter(**filters)
        q = request.query_params.get('q')
        if q:
            q_objects = Q()
            fields = ['code', 'totalAmount']
            for field in fields:
                q_objects |= Q(**{f'{field}__icontains': q})

            queryset = queryset.filter(q_objects)

        if request.user.role == User.UserRole.CLIENT:
            queryset = queryset.filter(Q(user=request.user) & (
                Q(paymentStatus=PaymentStatus.REJECTED) |
                Q(paymentStatus=PaymentStatus.REFUNDED) |
                Q(paymentStatus=PaymentStatus.CONFIRMED) |
                Q(paymentType=PaymentTypes.CASH)))
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if start and end:
            queryset = queryset.filter(
                created_at__gte=start,
                created_at__lte=end
            )

        return queryset
