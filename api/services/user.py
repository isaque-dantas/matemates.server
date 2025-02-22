from django.contrib.auth.models import AnonymousUser

from api import log
from api.models import User, InvitedEmail
from matemates_server import settings


class UserService:
    @staticmethod
    def create(serializer):
        validated_data = serializer.validated_data

        data = {
            **validated_data,
            'is_staff': (
                    validated_data['email'] == settings.ADMIN_EMAIL
                    or
                    InvitedEmail.objects.filter(email=validated_data['email']).exists()
            )
        }

        return User.objects.create_user(**data)

    @staticmethod
    def update(instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.name = validated_data['name']

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        profile_image_base64 = validated_data.get('profile_image_base64', None)
        if profile_image_base64:
            instance.profile_image = validated_data['profile_image_base64']

        instance.save()

        return instance

    @staticmethod
    def inactivate_user(username: str):
        instance = User.objects.get(username=username)
        instance.is_active = False
        instance.save()

    @staticmethod
    def turn_admin(email: str, user_who_invited: User):
        if User.objects.filter(email=email).exists():
            instance = User.objects.get(email=email)
            instance.is_staff = True

            instance.save()
            return instance

        invited_email = InvitedEmail(email=email, user_who_invited=user_who_invited)
        invited_email.save()

    @staticmethod
    def can_see_non_validated_entries(user: AnonymousUser | User) -> bool:
        return user.is_authenticated and user.is_staff

    @staticmethod
    def update_profile_image(serializer):
        data = serializer.validated_data
        instance: User = serializer.instance

        instance.profile_image.delete()
        instance.profile_image.save("foo.png", data["profile_image_base64"])
