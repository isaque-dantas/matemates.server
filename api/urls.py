from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('hello-world', views.hello_world),
    path('users', views.UserView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    # path('token', token_refresh)
]
