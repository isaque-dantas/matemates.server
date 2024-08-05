from rest_framework import serializers

import api.models
from api.serializers.definition import DefinitionSerializer
from api.serializers.question import QuestionSerializer
from api.serializers.syllable import SyllableSerializer
from api.serializers.term import TermSerializer


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Entry
        fields = '__all__'

    def create(self, validated_data: dict):
        associated_serializers = [
            SyllableSerializer,
            TermSerializer,
            QuestionSerializer,
            DefinitionSerializer
        ]

        for serializer in associated_serializers:
            serializer().create(validated_data)

        instance = self.Meta.model.objects.create(**validated_data)
        return instance
