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

    main_term_gender = serializers.CharField(read_only=True)
    main_term_grammatical_category = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    definitions = DefinitionSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        request = self.context.get("request")
        if request and request.method == "PATCH":
            return {"content": internal_value.get("content").strip()}

        return {
            "content": internal_value.get("content").strip(),
            "main_term_gender": data.get("main_term_gender"),
            "main_term_grammatical_category": data.get("main_term_grammatical_category"),
            "images": ImageSerializer(data=data["images"], many=True, read_only=True),
            "definitions": DefinitionSerializer(data=data["definitions"], many=True, read_only=True),
            "questions": QuestionSerializer(data=data["questions"], many=True, read_only=True),
        }

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method == "PATCH":
           return data

        data["definitions"].validate(data["definitions"])
        log.debug(f'{data["definitions"]=}')
        return data

    def validate_content(self, value):
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
