from rest_framework import serializers

from api.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
