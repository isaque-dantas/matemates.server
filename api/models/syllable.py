from django.db import models

import api.models


class SyllableManager(models.Manager):
    def get_syllables_data(self, term: api.models.Term, term_content: str):
        syllables_data = list()

        for i, syllable_content in enumerate(term_content.split(".")):
            syllable_data = dict()
            syllable_data.update({"content": self.parse_content(syllable_content)})
            syllable_data.update({"order": i})
            syllable_data.update({"term": term})

            syllables_data.append(syllable_data)

        return syllables_data

    @staticmethod
    def create(validated_data):
        syllable = api.models.Syllable(content=validated_data['content'], order=validated_data['order'])
        syllable.term = validated_data['term']
        syllable.save()

    @staticmethod
    def get_terms_contents_from_content(content):
        return content.replace("*", "").split()

    @staticmethod
    def parse_content(content: str):
        return content.replace("*", "")


class Syllable(models.Model):
    content = models.CharField(max_length=16, blank=False)
    order = models.IntegerField(blank=False)

    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    objects = SyllableManager()
