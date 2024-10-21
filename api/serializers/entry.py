from rest_framework import serializers

import api.models
from api import log
from api.serializers.definition import DefinitionSerializer
from api.serializers.image import ImageSerializer
from api.serializers.question import QuestionSerializer
from api.serializers.term import TermSerializer
from api.services.entry import EntryService


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Entry
        fields = ['id', 'content', 'is_validated', 'images', 'definitions', 'questions', 'main_term_gender',
                  'main_term_grammatical_category']

    main_term_gender = serializers.CharField(read_only=True)
    main_term_grammatical_category = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    definitions = DefinitionSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        log.debug(f'{internal_value=}')
        log.debug(f'{data=}')

        return {
            "content": internal_value["content"],
            "main_term_gender": data["main_term_gender"],
            "main_term_grammatical_category": data["main_term_grammatical_category"],
            "images": ImageSerializer(data=data["images"], many=True, read_only=True),
            "definitions": DefinitionSerializer(data=data["definitions"], many=True, read_only=True),
            "questions": QuestionSerializer(data=data["questions"], many=True, read_only=True),
        }

    def validate(self, data):
        data["definitions"].validate(data["definitions"])
        log.debug(f'{data["definitions"]=}')
        return data

    # @staticmethod
    def validate_content(self, value):
        errors = []

        # log.debug(f'{it_is_updating_to_the_same_value=}')
        # log.debug(f'{self.instance=}')
        # log.debug(f'{EntryService.parse_content(value)=}')

        it_is_updating_to_the_same_value = (
                self.instance is not None
                and
                EntryService.parse_content(value) == self.instance.content
        )

        if EntryService.content_already_exists(value) and not it_is_updating_to_the_same_value:
            errors.append(f"'{value}' already exists")

        stars_errors: list = EntryService.get_stars_formatting_errors(value)
        if stars_errors:
            errors.extend(stars_errors)

        log.debug(f"{stars_errors=}")

        dots_errors: list = EntryService.get_dots_formatting_errors(value)
        if dots_errors:
            errors.extend(dots_errors)

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def to_representation(self, instance):
        log.debug(f'{instance=}')
        log.debug(f'{instance.content=}')
        log.debug(f'{instance.definitions.all()=}')

        if not isinstance(instance, api.models.Entry):
            return super().to_representation(instance)

        related_entities = EntryService.get_related_entities(instance)
        log.debug(f"\n{related_entities=}\n")

        return {
            "id": instance.pk,
            "content": instance.content,
            "is_validated": instance.is_validated,
            "terms": TermSerializer(related_entities["terms"], many=True).data,
            "definitions": DefinitionSerializer(related_entities["definitions"], many=True).data,
            "questions": QuestionSerializer(related_entities["questions"], many=True).data,
            "images": ImageSerializer(related_entities["images"], many=True).data
        }
