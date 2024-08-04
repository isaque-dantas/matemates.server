from django.db import models

from .entry import Entry


class Term(models.Model):
    class Gender(models.TextChoices):
        MALE = ('M', "Masculino")
        FEMALE = ('F', "Feminino")

    class GrammaticalCategory(models.TextChoices):
        SUBSTANTIVE = 'substantivo'
        VERB = 'verbo'
        ADJECTIVE = 'adjetivo'
        NUMERAL = 'numeral'

    content = models.CharField(max_length=64, blank=False, unique=True)
    gender = models.CharField(max_length=16, default=None, blank=False, choices=Gender)
    grammatical_category = models.CharField(max_length=16, blank=False, choices=GrammaticalCategory, default=None)
    is_main_term = models.BooleanField(default=False, blank=False)
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
