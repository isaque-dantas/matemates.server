from django.db import models

from api.models import Entry


class TermManager(models.Manager):
    @staticmethod
    def create(term):
        term.save()
        return term

    @staticmethod
    def parse_terms_from_content(content: str):
        return content.split()

    @staticmethod
    def get_content_without_mask(content: str):
        return content.replace("*", "").replace(".", "")


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
    gender = models.CharField(max_length=16, blank=True, choices=Gender)
    grammatical_category = models.CharField(max_length=16, blank=True, choices=GrammaticalCategory)
    is_main_term = models.BooleanField(default=False, blank=False)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    objects = TermManager()
