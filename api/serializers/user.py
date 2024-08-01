from rest_framework import serializers

from api.models.user import User
from matemates_server import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_admin']
        REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        validated_data.update(
            {'is_admin': validated_data['email'] == settings.ADMIN_EMAIL}
        )

        instance = self.Meta.model(**validated_data)

        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def inactivate_user(self, username: str):
        instance = self.Meta.model.objects.get(username=username)
        instance.is_active = False
        instance.save()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

    def turn_admin(self, email):
        instance = self.Meta.model.objects.get(email=email)
        instance.is_admin = True
        instance.save()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

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
