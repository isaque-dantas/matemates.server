from django.db import models

from .entry import Entry


class Image(models.Model):
    path = models.CharField(max_length=128, blank=False, unique=True)
    caption = models.CharField(max_length=256, blank=True)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
