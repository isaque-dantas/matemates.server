from api.models import Entry, Definition
from api.services.definition import DefinitionService
from api.services.image import ImageService
from api.services.question import QuestionService
from api.services.term import TermService
from api import log

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
    def is_content_invalid(content: str):
        return Entry.objects.filter(content=EntryService.parse_content(content)).exists()

    @staticmethod
    def exists(pk: int):
        return Entry.objects.filter(pk=pk).exists()

    @staticmethod
    def get_all():
        return Entry.objects.all()

    @staticmethod
    def get(pk: int):
        return Entry.objects.get(pk=pk)

    @staticmethod
    def update(serializer):
        pass

    @staticmethod
    def delete(serializer):
        pass

    @staticmethod
    def get_related_entities(instance: Entry):
        all_definitions = Definition.objects.all()
        log.debug(f"{all_definitions=}")

        return {
            "terms": instance.terms.all(),
            "images": instance.images.all(),
            "questions": instance.questions.all(),
            "definitions": instance.definition_set.all(),
        }

    @staticmethod
    def get_all_related_to_knowledge_area(knowledge_area_content: str):
        definitions = Definition.objects.filter(
            knowledge_area__content=knowledge_area_content
        ).select_related("entry")

        return [definition.entry for definition in definitions]
