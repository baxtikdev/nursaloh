from django.urls import path, include

from api.router import urlpatterns

urlpatterns += [
    path('payment', include("api.payment.click.urls")),
    path('user', include("api.users.urls")),
]
