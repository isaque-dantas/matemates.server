from django.db.models import Model
from rest_framework import serializers

from api import log
from api.models import Entry, Definition, Image
from api.serializers.definition import DefinitionSerializer
from api.serializers.image import ImageSerializer
from api.serializers.question import QuestionSerializer
from api.serializers.term import TermSerializer
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
        EntryService.create_related_entities(entry_data, entry)

        return entry

    @staticmethod
    def create_related_entities(entry_data: dict, instance: Entry):
        TermService.create_all(entry_data, instance)
        ImageService.create_all(entry_data, instance)
        DefinitionService.create_all(entry_data, instance)
        QuestionService.create_all(entry_data, instance)

    @staticmethod
    def parse_content(content: str):
        return content.replace("*", "").replace(".", "")

    @staticmethod
    def content_already_exists(content: str):
        return Entry.objects.filter(content=EntryService.parse_content(content)).exists()

    @staticmethod
    def get_stars_formatting_errors(content: str) -> list:
        if " " not in content:
            return []

        log.debug(f'{content.count("*")=}')

        errors = []
        if content.count("*") != 2:
            errors.append(f"'{content}' should have exactly 2 '*' characters")
            return errors

        first_star_index = content.find("*")
        last_star_index = content.find("*", first_star_index + 1)
        main_term = content[first_star_index + 1:last_star_index]

        if ' ' in main_term:
            errors.append(f"text '{main_term}' inside the two '*' should not have spaces")

        return errors

    @staticmethod
    def get_dots_formatting_errors(content: str) -> list:
        errors = []
        content_without_first_and_last_dots = content

        if content[0] == ".":
            errors.append("dots should not be the first characters")
            content_without_first_and_last_dots = content[1:]

        if content[-1] == ".":
            errors.append("dots should not be the last characters")
            content_without_first_and_last_dots = content[:-1]

        dots_indexes = []
        for i, char in enumerate(content_without_first_and_last_dots):
            if char == ".":
                dots_indexes.append(i)

        if any(
                [
                    not content[index - 1].isalpha()
                    or
                    not content[index + 1].isalpha()

                    for index in dots_indexes
                ]
        ):
            errors.append(f"dots should be between alphabet characters only")

        return errors

    @staticmethod
    def exists(pk: int):
        return Entry.objects.filter(pk=pk).exists()

    @staticmethod
    def get_all(should_get_only_validated: bool):
        if should_get_only_validated:
            return Entry.objects.filter(is_validated=True).all()

        return Entry.objects.all()

    @staticmethod
    def get(pk: int):
        return Entry.objects.get(pk=pk)

    @staticmethod
    def get_all_related_to_knowledge_area(knowledge_area_content: str, should_get_only_validated: bool):
        definitions = Definition.objects.filter(
            knowledge_area__content=knowledge_area_content
        ).select_related("entry")

        log.debug(f"{len(definitions)=}")

        entries = [definition.entry for definition in definitions]

        entries_ids = [entry.pk for entry in entries]
        duplicated_ids = filter(lambda e: entries_ids.count(e) >= 2, entries_ids)
        duplicated_ids = list(set(duplicated_ids))

        non_duplicated_entries = [
            entry
            for entry in entries
            if entry.pk not in duplicated_ids
        ]

        for duplicated_id in duplicated_ids:
            entry = next(filter(lambda e: e.pk == duplicated_id, entries))
            non_duplicated_entries.append(entry)

        if should_get_only_validated:
            return list(filter(lambda e: e.is_validated, non_duplicated_entries))

        return non_duplicated_entries


    @staticmethod
    def get_data_from_instances(entries: list[Entry]):
        return [EntryService.to_representation(entry) for entry in entries]

    @staticmethod
    def update(serializer: serializers.ModelSerializer):
        instance = serializer.instance
        entry_data = serializer.validated_data

        images_ids_that_must_not_be_updated = [
            data["id"] for data in entry_data["images"]
            if data["base64_image"] == ''
        ]

        log.debug(f"{entry_data['images']=}")
        log.debug(f"{images_ids_that_must_not_be_updated=}")

        entry_data["images"] = [
            image for image in entry_data["images"]
            if image["id"] not in images_ids_that_must_not_be_updated
        ]

        EntryService.delete_related_entities(instance, images_ids_that_must_not_be_deleted=images_ids_that_must_not_be_updated)
        EntryService.create_related_entities(entry_data, instance)

        instance.content = EntryService.parse_content(entry_data['content'])
        instance.save()

    @staticmethod
    def delete(pk: int):
        EntryService.get(pk).delete()

    @staticmethod
    def delete_related_entities(instance: Entry, images_ids_that_must_not_be_deleted: list[int] | None = None):
        related_entities: dict[str, Model] = EntryService.get_related_entities(instance)

        for entity_name, entities in related_entities.items():

            if entity_name == "images":
                for image in entities:
                    if image.id not in images_ids_that_must_not_be_deleted:
                        log.debug(f"{image.id=}")
                        image.delete()

                continue
            else:
                log.debug(f"{entities=}")
                entities.delete()

    @staticmethod
    def get_related_entities(instance: Entry) -> dict[str, Model]:
        all_definitions = Definition.objects.all()
        log.debug(f"{all_definitions=}")

        return {
            "terms": instance.terms.all(),
            "images": instance.images.all(),
            "questions": instance.questions.all(),
            "definitions": instance.definitions.all(),
        }

    @staticmethod
    def to_representation(instance: Entry, context: dict | None = None):
        related_entities = EntryService.get_related_entities(instance)
        log.debug(f"\n{related_entities=}\n")

        return {
            "id": instance.pk,
            "content": instance.content,
            "is_validated": instance.is_validated,
            "terms": TermSerializer(related_entities["terms"], many=True).data,
            "definitions": DefinitionSerializer(related_entities["definitions"], many=True).data,
            "questions": QuestionSerializer(related_entities["questions"], many=True).data,
            "images": ImageSerializer(related_entities["images"], many=True, context=context).data
        }
