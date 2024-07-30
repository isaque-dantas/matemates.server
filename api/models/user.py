from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str, first_name: str, last_name: str,
                    profile_image_path: str):
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name,
                          last_name=last_name, profile_image_path=profile_image_path)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, username: str, password: str, first_name: str, last_name: str,
                         profile_image_path: str):
        user = self.create_user(email, username, password, first_name, last_name, profile_image_path)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, blank=False)
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    profile_image_path = models.CharField(max_length=128, blank=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
