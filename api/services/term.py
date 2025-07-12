import logging
import re
from api import log
from api.models import Term, Syllable
from api.services.syllable import SyllableService


class TermService:
    @staticmethod
    def create_all(entry_data, entry):
        data_list = [
            {
                'is_main_term': True,
                'gender': entry_data['main_term_gender'],
                'grammatical_category': entry_data['main_term_grammatical_category'],
                'content': term_content.replace("*", "")
            }

            if '*' in term_content or len(entry_data['content'].split()) == 1 else

            {
                'is_main_term': False,
                'content': term_content.replace("*", "")
            }

            for term_content in entry_data['content'].split()
        ]

        log.debug(f"terms: {data_list}")

        return [TermService.get_instance_from_data(data, entry) for data in data_list]

    @staticmethod
    def get_instance_from_data(data, entry):
        original_content = data["content"]
        data["content"] = data["content"].replace(".", "")

        term = Term.objects.create(
            Term(**data, entry=entry)
        )

        SyllableService.create_from_term_content(original_content, term)

        return term

    @classmethod
    def get(cls, pk):
        return Term.objects.get(pk=pk)

    @classmethod
    def get_main_from_entry(cls, entry):
        return Term.objects.get(entry=entry, is_main_term=True)

    @classmethod
    def update_related_to_entry(cls, entry, entry_data: dict):
        log.debug(f"{cls.has_terms_quantity_changed(entry.content, entry_data['content'])}")
        old_main_term = cls.get_main_from_entry(entry)

        if cls.has_terms_quantity_changed(entry.content, entry_data["content"]):
            cls.delete_related_terms_and_syllables(entry.pk)
            cls.create_all(
                entry_data={
                    "content": entry_data["content"],
                    "main_term_gender":
                        entry_data.get("main_term_gender") or old_main_term.gender,
                    "main_term_grammatical_category":
                        entry_data.get("main_term_grammatical_category") or old_main_term.grammatical_category,
                }, entry=entry
            )

            return None

        for term, new_term_content in zip(Term.objects.filter(entry=entry), entry_data["content"].split()):
            print()
            log.debug(f"{new_term_content=}")
            log.debug(f"{term.content=}")
            print()

            term.content = new_term_content.replace("*", "").replace(".", "")
            term.is_main_term = cls.content_is_of_main_term(new_term_content)
            if term.is_main_term:
                term.gender = entry_data.get("main_term_gender") or old_main_term.gender
                term.grammatical_category = entry_data.get(
                    "main_term_grammatical_category") or old_main_term.grammatical_category
            else:
                term.gender = ""
                term.grammatical_category = ""

            term.save()

            Syllable.objects.filter(term__id=term.pk).delete()
            SyllableService.create_from_term_content(new_term_content.replace("*", ""), term)

    @staticmethod
    def has_terms_quantity_changed(old_entry_content: str, new_entry_content: str) -> bool:
        return len(old_entry_content.split(" ")) != len(new_entry_content.split(" "))

    @staticmethod
    def delete_related_terms_and_syllables(entry_pk: int):
        Syllable.objects.filter(term__entry__id=entry_pk).delete()
        Term.objects.filter(entry__id=entry_pk).delete()

    @staticmethod
    def content_is_of_main_term(content: str) -> bool:
        return re.search(r"\A\*[a-zA-Z.]+\*\Z", content) is not None
