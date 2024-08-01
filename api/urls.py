from django.urls import path
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import user

urlpatterns = [
    path('hello-world', user.hello_world),
    path('users', user.UserView.as_view()),
    path('users/turn-admin', user.turn_admin),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
