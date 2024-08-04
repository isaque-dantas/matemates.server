from django.db import models

from .term import Term


class Syllable(models.Model):
    content = models.CharField(max_length=16, blank=False)
    order = models.IntegerField(blank=False)

    term = models.ForeignKey(Term, on_delete=models.CASCADE)
