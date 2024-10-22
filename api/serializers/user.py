from rest_framework import serializers

from api import log
from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'is_staff', 'profile_image_base64_encoded_string']
        REQUIRED_FIELDS = ['username', 'email', 'password']

    profile_image_base64_encoded_string = serializers.CharField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        log.debug(f"{representation=}")

        representation.pop('password', None)
        representation.pop('profile_image_base64_encoded_string', None)
        return representation
