from api.models import Syllable


class SyllableService:
    @staticmethod
    def create_from_term_content(term_content: str, term):
        data_list = [
            {'content': syllable_content}
            for syllable_content in term_content.split(".")
        ]

        return Syllable.objects.create(
            [SyllableService.create(data, term) for data in data_list]
        )

    @staticmethod
    def create(data, term):
        return Syllable(
            content=data["content"],
            term=term
        )
