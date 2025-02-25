from api import log
from api.models import Image, Entry
from api.models.image import image_directory_path


class ImageService:
    @staticmethod
    def create_all(entry_data, entry):
        log.debug(f"{entry_data['images']=}")

        data_list = [
            {
                'caption': data['caption'] if data['caption'] else None,
                **data
            }

            for data in entry_data["images"]
        ]

        return Image.objects.create(
            [ImageService.create(data, entry, i) for i, data in enumerate(data_list)],
        )

    @staticmethod
    def create(data, entry, image_number) -> dict[str, Image | str]:
        image = Image.objects.model(
            caption=data["caption"],
            entry=entry,
            image_number_in_entry=image_number
        )

        return {
            "image": image,
            "content": data["base64_image"],
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
