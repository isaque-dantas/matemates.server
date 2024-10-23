from django.db import models

class EntryManager(models.Manager):
    def create(self, **kwargs):
        pass

class Entry(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    is_validated = models.BooleanField(default=False, blank=False)

    objects = EntryManager()

    def __repr__(self):
        return f'<Entry {self.content}>'
