from random import random

from api.models import Image
from api import log

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
            [ImageService.create(data, entry) for data in data_list],
        )

    @staticmethod
    def create(data, entry):
        image_path = ImageService.store_image_file(
            data["base64_encoded_string"]
        )

        return Image(caption=data["caption"], path=image_path, entry=entry)

    @staticmethod
    def store_image_file(base64_encoded_string: str):
        # TODO: Code to store image
        return f'foo {int(random() * 1000 + 5)}'
