from api import log
from api.models import Syllable
from api.serializers.syllable import SyllableSerializer


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

    @staticmethod
    def get_data_related_to_term(term):
        syllables = Syllable.objects.filter(term__id=term.pk).all()
        log.debug(f"{syllables=}")
        syllables_data = SyllableSerializer(syllables, many=True).data
        return syllables_data
