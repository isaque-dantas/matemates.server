from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail

from api.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def inactivate_user(self, username: str):
        instance = self.Meta.model.objects.get(username=username)
        instance.is_active = False
        instance.save()


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']

    def update(self, instance: User, validated_data):
        # duplications = self.Meta.model.objects.is_duplicated(validated_data['email'], validated_data['username'])
        # for key, duplicated_user_id in duplications.items():
        #     if duplicated_user_id == instance.id:
        #         self.errors.update({key: ErrorDetail(string=f'user with this {key} already exists.', code='unique')})

        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        instance.set_password(validated_data['password'])

    def validate_email(self, data):
        if self.is_duplicated(data['email'], 'email'):
            raise serializers.ValidationError(f'user with email {data["email"]} already exists.')

    def validate_username(self, data):
        if self.is_duplicated(data['username'], 'username'):
            raise serializers.ValidationError(f'user with username {data["username"]} already exists.')

    def is_duplicated(self, attr, attr_name) -> bool:
        user = self.Meta.model.objects.get({attr_name: attr})
        if user:
            return True
        return False
