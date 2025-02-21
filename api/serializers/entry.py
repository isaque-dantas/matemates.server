from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    content = serializers.CharField(required=False)

    main_term_gender = serializers.CharField(read_only=True)
    main_term_grammatical_category = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    definitions = DefinitionSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        is_patch = self.context.get("is_patch")

        log.debug(f"{self.context=}")
        log.debug(f"{is_patch=}")

        if self.context.get("is_patch"):
            return {
                "content": internal_value.get("content"),
                "main_term_gender": internal_value.get("main_term_gender"),
                "main_term_grammatical_category": internal_value.get("main_term_grammatical_category"),
            }

        return {
            "content": internal_value.get("content"),
            "main_term_gender": data.get("main_term_gender"),
            "main_term_grammatical_category": data.get("main_term_grammatical_category"),
            "images": ImageSerializer(data=data.get("images"), many=True, read_only=True),
            "definitions": DefinitionSerializer(data=data.get("definitions"), many=True, read_only=True),
            "questions": QuestionSerializer(data=data.get("questions"), many=True, read_only=True),
        }

    def validate(self, data):
        if self.context.get("is_patch"):
           return data

        errors = []

        if not data['images'].initial_data:
            errors.append(f"O campo 'images' é obrigatório.")

        if not data['definitions'].initial_data:
            errors.append(f"O campo 'definitions' é obrigatório.")
        else:
            data["definitions"].validate(data["definitions"])

        if not data['questions'].initial_data:
            errors.append(f"O campo 'questions' é obrigatório.")

        if errors:
            raise ValidationError(errors)

        return data

    def validate_content(self, value):
        if not self.context.get("is_patch") and value is None:
            raise ValidationError("O campo 'content' é obrigatório.")

        try:
            EntryService.validate_content(self.instance, value)
        except ValidationError as err:
            raise err

        return value

    def to_representation(self, instance):
        # log.debug(f'{instance=}')
        # log.debug(f'{instance.content=}')
        # log.debug(f'{instance.definitions.all()=}')

        if not isinstance(instance, api.models.Entry):
            return super().to_representation(instance)

        return EntryService.to_representation(instance, context=self.context)
