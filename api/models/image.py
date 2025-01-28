import base64

from django.core.files.base import ContentFile
from django.db import models

from api import log
from api.models.entry import Entry


class ImageManager(models.Manager):
    @staticmethod
    def create(images_data: list[dict]):
        images = []
        for image_data in images_data:
            image = image_data['image']
            # image_format = image_data['format']
            image_content = image_data['content']

            base64_str = image_content.split(",")[-1]
            decoded_image = base64.b64decode(base64_str)

            image.content.save(f"foo.png", ContentFile(decoded_image))
            log.debug(f"{image=}")

            image.save()

            images.append(image)

        return images


def image_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"entry_{instance.entry.pk}__image_{instance.image_number_in_entry}__.{extension}"


class Image(models.Model):
    content = models.ImageField(upload_to=image_directory_path, blank=True)
    caption = models.CharField(max_length=256, blank=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="images")

    image_number_in_entry = models.IntegerField()

    objects = ImageManager()
