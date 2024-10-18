from rest_framework import serializers

import api.models
from api import log
from api.serializers.definition import DefinitionSerializer
from api.serializers.image import ImageSerializer
from api.serializers.question import QuestionSerializer


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Entry
        fields = ['id', 'content', 'is_validated', 'images', 'definitions', 'questions', 'main_term_gender',
                  'main_term_grammatical_category']

    main_term_gender = serializers.CharField(read_only=True)
    main_term_grammatical_category = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    definitions = DefinitionSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        return {
            **internal_value,
            "images": ImageSerializer(data=data["images"], many=True, read_only=True),
            "definitions": DefinitionSerializer(data=data["definitions"], many=True, read_only=True),
            "questions": QuestionSerializer(data=data["questions"], many=True, read_only=True),
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        log.debug(f'{representation=}')

        return representation
