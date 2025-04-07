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
        return content.strip().replace("*", "").replace(".", "")

    @staticmethod
    def content_already_exists(content: str):
        return Entry.objects.filter(content=EntryService.parse_content(content)).exists()

    @staticmethod
    def validate_content(instance: Entry, value: str):
        errors = []

        value = value.strip()

        it_is_updating_to_the_same_value = (
                instance is not None
                and
                EntryService.parse_content(value) == instance.content
        )

        if EntryService.content_already_exists(value) and not it_is_updating_to_the_same_value:
            errors.append(f"'{value}' already exists")

        log.debug(f"{value=}")

        stars_errors: list = EntryService.get_stars_formatting_errors(value)
        if stars_errors:
            errors.extend(stars_errors)

        log.debug(f"{stars_errors=}")

        dots_errors: list = EntryService.get_dots_formatting_errors(value)
        if dots_errors:
            errors.extend(dots_errors)

        if errors:
            raise serializers.ValidationError(errors)

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
        if should_get_only_validated:
            return (
                Entry.objects
                .filter(
                    is_validated=should_get_only_validated,
                    definitions__knowledge_area__content=knowledge_area_content
                )
                .distinct().all()
            )

        return (
            Entry.objects
            .filter(definitions__knowledge_area__content=knowledge_area_content)
            .distinct().all()
        )

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

        # log.debug(f"{entry_data['images']=}")
        log.debug(f"{images_ids_that_must_not_be_updated=}")

        entry_data["images"] = [
            image for image in entry_data["images"]
            if image["id"] not in images_ids_that_must_not_be_updated
        ]

        EntryService.delete_related_entities(instance,
                                             images_ids_that_must_not_be_deleted=images_ids_that_must_not_be_updated)
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

    @staticmethod
    def search_by_content(search_query: str, should_get_only_validated: bool):
        if should_get_only_validated:
            return (
                Entry.objects
                .filter(content__contains=search_query, is_validated=True)
                .distinct()
                .all()
            )

        return (
            Entry.objects.filter(content__contains=search_query).distinct().all()
        )

    @classmethod
    def patch(cls, serializer):
        data = serializer.validated_data
        instance: Entry = serializer.instance

        log.debug(f"{data=}")

        if data.get("content"):
            TermService.update_related_to_entry(instance, data)

            instance.content = cls.parse_content(data.get("content"))
            instance.save()
            return None

        main_term = TermService.get_main_from_entry(instance)

        if (
                not data.get("main_term_grammatical_category") and
                not data.get("main_term_gender")
        ):
            return None

        if data.get("main_term_grammatical_category"):
            main_term.grammatical_category = data.get("main_term_grammatical_category")

        if data.get("main_term_gender"):
            main_term.gender = data.get("main_term_gender")

        log.debug(f"{main_term=}")
        log.debug(f"{data.get('main_term_grammatical_category')=}")
        log.debug(f"{data.get('main_term_gender')=}")
        main_term.save()

    @classmethod
    def make_entry_validated(cls, pk: int):
        entry = cls.get(pk)
        entry.is_validated = True
        entry.save()
