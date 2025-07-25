from drf_base64.fields import Base64ImageField
from rest_framework.exceptions import ValidationError

from api import log
from api.models import Image, Entry
from api.models.image import image_directory_path


class ImageService:
    @staticmethod
    def create_all(entry_data, entry):
        # log.debug(f"{entry_data['images']=}")

        data_list = [
            {
                'caption': data['caption'] if data['caption'] else None,
                **data
            }

            for data in entry_data["images"]
        ]

        return Image.objects.create(
            [ImageService.get_instance_from_data(data, entry, i) for i, data in enumerate(data_list)],
        )

    @staticmethod
    def get_instance_from_data(data, entry, image_number) -> dict[str, Image | str]:
        image = Image.objects.model(
            caption=data["caption"],
            entry=entry,
            image_number_in_entry=image_number
        )

        decoded_image = Base64ImageField()._decode(data["base64_image"])

        return {
            "image": image,
            "content": decoded_image,
        }

    @staticmethod
    def get_all_related(entry: Entry):
        return Image.objects.filter(entry=entry)

    @staticmethod
    def get(image_pk: int):
        return Image.objects.get(pk=image_pk)

    @staticmethod
    def exists(image_pk: int):
        return Image.objects.filter(pk=image_pk).exists()

    @staticmethod
    def is_parent_validated(pk):
        return Image.objects.get(pk=pk).entry.is_validated

    @classmethod
    def update(cls, serializer):
        instance: Image = serializer.instance
        data = serializer.validated_data

        log.debug(f"ImageService.update: {data}")

        if "content" in data:
            instance.content.delete()

            filename = image_directory_path(instance, data["content"].name)
            instance.content.save(filename, data["content"])

        if "caption" in data:
            instance.caption = data["caption"]

        instance.save()

    @classmethod
    def create(cls, serializer):
        data = serializer.validated_data
        image_number = Image.objects.filter(entry__pk=data["entry"].pk).count()

        log.debug(f"{data=}")

        image = Image(
            caption=data["caption"],
            entry=data["entry"],
            image_number_in_entry=image_number
        )

        filename = image_directory_path(image, data["content"].name)
        image.content.save(filename, data["content"])

        if "caption" in data:
            image.caption = data["caption"]

        image.save()

        return image

    @classmethod
    def delete(cls, pk):
        image = cls.get(pk)
        image.content.delete()
        image.delete()

    @classmethod
    def is_content_base64_encoded(cls, content: str):
        return (
            content.startswith("data:image/")
            and
            ';base64,' in content
        )

    @classmethod
    def validate(cls, attrs):
        errors = [
            {"base64_image": "A imagem deve estar no formato base64."}

            for i, attr in enumerate(attrs)

            if not cls.is_content_base64_encoded(attr.get('base64_image'))
        ]

        if len(errors) == 0:
            return None

        raise ValidationError({'images': errors})
