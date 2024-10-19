from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from api.services.image import ImageService
from matemates_server import settings


class UserManager(BaseUserManager):
    @staticmethod
    def create_user(**validated_data):
        if validated_data['profile_image_base64_encoded_string']:
            path = ImageService.store_image_file(validated_data['profile_image_base64_encoded_string'])
        else:
            path = ''

        user = User.objects.model(
            email=User.objects.normalize_email(validated_data['email']),
            username=validated_data['username'],
            name=validated_data['name'],
            profile_image_path=path,
            is_staff=validated_data['is_admin'],
        )

        user.set_password(validated_data['password'])
        user.is_active = True

        user.save()

        return user

    def create_superuser(self, **data):
        user = self.create_user(**data)

        user.is_staff()
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    profile_image_path = models.CharField(max_length=128, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
