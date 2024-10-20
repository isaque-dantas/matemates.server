from django.db import models

from api.models.entry import Entry


class ImageManager(models.Manager):
    def create(self, images):
        self.bulk_create(images)


class Image(models.Model):
    path = models.CharField(max_length=128, blank=False, unique=True)
    caption = models.CharField(max_length=256, blank=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="images")

    objects = ImageManager()
