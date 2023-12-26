from django.db.models import Q
from rest_framework import filters


class ProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}
        fields = ['subcategory', 'subcategory__category', 'uom', 'brand', 'isTop', 'cornerStatus', 'status']

        for field in fields:
            param_value = request.query_params.get(field)
            if param_value:
                filters[f'{field}__exact'] = param_value
        queryset = queryset.filter(**filters)

        q = request.query_params.get('q')
        if q:
            q_objects = Q()
            fields = ['code', 'title', 'description', 'price', 'discountPrice', 'material', 'brand__title', 'size',
                      'manufacturer']

            for field in fields:
                q_objects |= Q(**{f'{field}__icontains': q})

            queryset = queryset.filter(q_objects)

        return queryset
