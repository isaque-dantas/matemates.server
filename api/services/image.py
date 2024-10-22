from api import log
from api.models import Image
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
    def create(data, entry, image_number):
        # return Image(
        #     caption=data["caption"],
        #     entry=entry,
        #     image_number_in_entry=image_number
        # )
        image = Image.objects.model(
            content=data["base64_image"],
            caption=data["caption"],
            entry=entry,
            image_number_in_entry=image_number
        )

        path = image_directory_path(image, "abcde.jpg")
        log.debug(f"{path=}")

        return image
