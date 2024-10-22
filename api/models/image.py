from django.db import models

from api.models.entry import Entry


class ImageManager(models.Manager):
    def create(self, images):
        # self.bulk_create(images)
        for image in images:
            image.save()

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
