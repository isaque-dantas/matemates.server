from django.db import models

import api
from api.models import Syllable


class EntryManager(models.Manager):
    def create(self, **kwargs):
        entry = Entry(content=self.parse_content(kwargs['content']))
        pass

    @staticmethod
    def parse_content(content: str):
        return content.replace("*", "").replace(" ", "_").replace(".", "")

    def get_terms_from_content(self, entry, entry_content: str, main_term_gender: str,
                                main_term_grammatical_category: str):
        for i, term_content in enumerate(entry_content.split(" ")):
            term_data = dict()
            term_data.update({"content": self.parse_content(term_content)})
            term_data.update({"order": i})

            is_main_term = term_content.startswith("*") and term_content.endswith("*")
            if is_main_term:
                term_data.update({"gender": main_term_gender})
                term_data.update({"grammatical_category": main_term_grammatical_category})
            term_data.update({"is_main_term": is_main_term})

            term = api.models.Term(**term_data)
            term.entry = entry
            term.save()

    def save_syllables_from_content(self, terms: list[api.models.Term], term_content: str):
        for term in terms:
            for i, syllable_content in enumerate(term_content.split(".")):
                syllable_data = dict()
                syllable_data.update({"content": self.parse_content(syllable_content)})
                syllable_data.update({"order": i})

                syllable = Syllable(**syllable_data)
                syllable.term = term
                syllable.save()



class Entry(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    is_validated = models.BooleanField(default=False, blank=False)

    objects = models.Manager()
