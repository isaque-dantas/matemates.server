from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'is_staff', 'profile_image_base64']
        REQUIRED_FIELDS = ['username', 'email', 'password']

    profile_image_base64 = Base64ImageField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        representation.pop('profile_image_base64', None)
        return representation
