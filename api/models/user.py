from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    @staticmethod
    def create_user(**validated_data):
        user = User.objects.model(
            email=User.objects.normalize_email(validated_data['email']),
            username=validated_data['username'],
            name=validated_data['name'],
            profile_image=validated_data.get("profile_image_base64"),
            is_staff=validated_data['is_staff'],
        )

        user.set_password(validated_data['password'])
        user.is_active = True

        user.save()

        return user

    def create_superuser(self, **data):
        user = self.create_user(**data)

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


def user_directory_path(instance, filename):
    return f"user_{instance.pk}__{filename}"


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    is_staff = models.BooleanField(default=False)

    profile_image = models.ImageField(blank=True, upload_to=user_directory_path)

    objects = UserManager()
    USERNAME_FIELD = 'email'
