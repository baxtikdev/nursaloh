from django.contrib.auth import get_user_model
from django.db.models import Q, Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin, IsOwn
from api.users import serializers as _serializer
from common.users.models import Address

User = get_user_model()


@extend_schema(tags=["User"])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = _serializer.UserCreateSerializer
    permission_classes = [IsAdmin]


@extend_schema(tags=["User"])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = _serializer.UserListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q)
            )
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


@extend_schema(tags=["User"])
class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = _serializer.UserDetailSerializer
    permission_classes = [IsAdmin | IsOwn]
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch(
                lookup="userAddress",
                queryset=Address.objects.all(),
            )
        )
        return queryset


@extend_schema(tags=["User"])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = _serializer.UserUpdateSerializer
    permission_classes = [IsAdmin | IsOwn]
    lookup_field = 'guid'


@extend_schema(tags=["User"])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = _serializer.UserCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
