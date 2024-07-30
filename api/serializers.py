from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
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
        if self.Meta.model.objects.filter(email=value).exists():
            raise serializers.ValidationError(f'user with email {value} already exists.')
        return value

    def validate_username(self, value):
        if self.Meta.model.objects.filter(username=value).exists():
            raise serializers.ValidationError(f'user with username {value} already exists.')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['password'] = ''
        return representation
