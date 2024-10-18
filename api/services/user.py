from api.models import User, InvitedEmail
from api.services.image import ImageService
from matemates_server import settings


class UserService:
    @staticmethod
    def create(validated_data):
        validated_data['is_admin'] = (
                validated_data['email'] == settings.ADMIN_EMAIL
                or
                InvitedEmail.objects.filter(email=validated_data['email']).exists()
        )

        return User.objects.create_user(**validated_data)

    @staticmethod
    def update(instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.name = validated_data['name']
        instance.set_password(validated_data['password'])

        path = ImageService.store_image_file(
            validated_data['profile_image_base64_encoded_string']
        )
        instance.profile_image_path = path

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
            instance.is_admin = True
            instance.save()
            return instance

        invited_email = InvitedEmail(email=email, user_who_invited=user_who_invited)
        invited_email.save()
