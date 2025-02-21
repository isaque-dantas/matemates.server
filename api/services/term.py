from api.models import Term
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
