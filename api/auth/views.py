from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers import LogOutSerializer, LoginSerializer, SignUpSerializer, UserLoginSerializer, \
    VerifyCodeSerializer, \
    ReSendCodeSerializer
from api.tasks import send_sms
from common.users.models import Code

User = get_user_model()


class LoginAPIView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if phone:
            user = User.objects.filter(phone=phone).first()
            if user and user.is_verified:
                return Response({"phone": ["A user with that phone already exists."]},
                                status=status.HTTP_400_BAD_REQUEST)

            name = request.data.get('name')
            if name:
                user.name = request.data.get('name')
                user.save()
                send_sms.apply_async([user.id, user.phone])
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_sms.apply_async([serializer.data.get("id"), serializer.data.get("phone")])
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyCodeAPIview(CreateAPIView):
    queryset = Code.objects.all()
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignInAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_sms.apply_async([serializer.validated_data.get('id'), serializer.validated_data.get('phone')])
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReSendCodeAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ReSendCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_sms.apply_async([serializer.validated_data.get('id'), serializer.validated_data.get('phone')])
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.data['refresh'])
        except:
            return Response({'message': "Token is blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        token.blacklist()
        return Response(status=status.HTTP_200_OK)
