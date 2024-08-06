from django.db import models

import api.models
from api.serializers.syllable import SyllableSerializer


class TermManager(models.Manager):
    def create(self, **kwargs):
        for i, term_content in enumerate(self.parse_terms_from_content(kwargs['content'])):
            term_data = {
                "content": self.get_content_without_mask(term_content),
                "order": i
            }

            is_main_term = term_content.startswith("*") and term_content.endswith("*")
            term_data.update({"is_main_term": is_main_term})
            if is_main_term:
                term_data.update({"gender": kwargs['main_term_gender']})
                term_data.update({"grammatical_category": kwargs['main_term_grammatical_category']})

            term = api.models.Term(**term_data)
            term.entry = kwargs['entry']
            term.save()

            SyllableSerializer().save_syllables(term, term_content)

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
    order = models.IntegerField(blank=False)

    entry = models.ForeignKey(api.models.Entry, on_delete=models.CASCADE)

    objects = TermManager()
