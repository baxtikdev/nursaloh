from django.urls import path

from api.users.views import UserDetailAPIView, UserUpdateAPIView

app_name = 'users'

urlpatterns = [
    # path("-create/", UserCreateAPIView.as_view(), name="user_create"),
    # path("-list/", UserListAPIView.as_view(), name="user_list"),
    path("-detail/<uuid:guid>/", UserDetailAPIView.as_view(), name="user_detail"),
    path("-update/<uuid:guid>/", UserUpdateAPIView.as_view(), name="user_update"),
    # path("-destroy/<uuid:guid>/", UserDeleteAPIView.as_view(), name="user_delete"),
]
