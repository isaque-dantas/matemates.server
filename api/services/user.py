from api.models import User
from api.services.image import ImageService
from matemates_server import settings


class UserService:
    @staticmethod
    def create(validated_data):
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
