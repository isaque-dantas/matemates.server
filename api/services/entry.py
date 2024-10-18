from api.models import Entry
from api.services.definition import DefinitionService
from api.services.image import ImageService
from api.services.question import QuestionService
from api.services.term import TermService


class EntryService:
    @staticmethod
    def create(serializer):
        entry_data = serializer.validated_data
        entry = Entry(
            content=EntryService.parse_content(entry_data['content']),
            is_validated=False,
        )

        entry.save()

        TermService.create_all(entry_data, entry)
        ImageService.create_all(entry_data, entry)
        DefinitionService.create_all(entry_data, entry)
        QuestionService.create_all(entry_data, entry)

        return entry

    @staticmethod
    def parse_content(content: str):
        return content.replace("*", "").replace(".", "")

    @staticmethod
    def get(serializer):
        pass

    @staticmethod
    def update(serializer):
        pass

    @staticmethod
    def delete(serializer):
        pass
