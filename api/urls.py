from django.urls import path
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import user
from api.views import entry

urlpatterns = [
    path('hello-world', user.hello_world),
    path('users', user.UserView.as_view()),
    path('users/turn-admin', user.turn_admin),
    path('entry', entry.EntryView.as_view()),
    path('entry/<int:pk>', entry.SingleEntryView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
