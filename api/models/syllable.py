from django.db import models

from api.models import Term


class SyllableManager(models.Manager):
    def create(self, syllables):
        return self.bulk_create(syllables)


class Syllable(models.Model):
    content = models.CharField(max_length=16, blank=False)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='syllables')

    objects = SyllableManager()
