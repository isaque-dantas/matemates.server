from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, StringRelatedField, RelatedField, ModelSerializer

from api.models import Definition
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.knowledge_area import KnowledgeAreaSerializer
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
        return {
            "content": instance.content,
            "knowledge_area": KnowledgeAreaSerializer(instance.knowledge_area).data
        }
