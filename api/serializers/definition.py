from rest_framework.serializers import StringRelatedField, ModelSerializer

from api import log
from api.models import Definition
from api.serializers.custom_list_serializer import CustomListSerializer
from api.services.definition import DefinitionService


class DefinitionListSerializer(CustomListSerializer):
    def validate(self, attrs):
        DefinitionService.validate(attrs)
        return attrs


class DefinitionSerializer(ModelSerializer):
    class Meta:
        model = Definition
        fields = ['content', 'knowledge_area__content']
        list_serializer_class = DefinitionListSerializer

    knowledge_area__content = StringRelatedField()

    def to_representation(self, instance):
        log.debug(f"instance in DefinitionSerializer: {instance}")
        return {
            "content": instance.content,
            "knowledge_area": {
                "content": instance.knowledge_area.content,
                "subject": instance.knowledge_area.subject
            }
        }
