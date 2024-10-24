from rest_framework import serializers

from api.models.user import User
from matemates_server import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'is_admin', 'profile_image_base64_encoded_string']
        REQUIRED_FIELDS = ['username', 'email', 'password']

    profile_image_base64_encoded_string = serializers.CharField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        representation.pop('profile_image_base64_encoded_string', None)
        return representation



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'username', 'email', 'password']

    def update(self, instance: User, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def validate_email(self, value):
        user_id = self.instance.id
        if User.objects.exclude(pk=user_id).filter(email=value).exists():
            raise serializers.ValidationError(f'user with email {value} already exists.')
        return value

    def validate_username(self, value):
        user_id = self.instance.id
        if User.objects.exclude(pk=user_id).filter(username=value).exists():
            raise serializers.ValidationError(f'user with username {value} already exists.')
        return value
