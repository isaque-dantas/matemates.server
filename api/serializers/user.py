from django.core.validators import validate_email, EmailValidator
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from api import log
from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'is_staff', 'profile_image_base64']
        # REQUIRED_FIELDS = ['name', 'username', 'email', 'password']

    profile_image_base64 = Base64ImageField(required=False)
    name = CharField(required=False)
    username = CharField(required=False)
    email = CharField(required=False, validators=[EmailValidator()])
    password = CharField(required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            "name": internal_value.get("name"),
            "username": internal_value.get("username"),
            "email": internal_value.get("email"),
            "password": internal_value.get("password"),
            "profile_image_base64": internal_value.get("profile_image_base64"),
        }

    def validate(self, attrs):
        if self.context.get('is_profile_image_update'):
            return attrs

        required_fields = ['name', 'username', 'email']
        errors = [
            f"O campo '{field}' é obrigatório."
            for field in required_fields
            if not attrs.get(field)
        ]

        if not self.context.get('is_update') and not attrs.get('password'):
            errors.append('A senha é obrigatória')

        if errors:
            raise ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.pop('password', None)
        representation.pop('profile_image_base64', None)
        return representation
