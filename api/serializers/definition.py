from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, StringRelatedField, RelatedField

from api.models import Definition
from api.serializers.custom_list_serializer import CustomListSerializer
from api.services.definition import DefinitionService

class DefinitionListSerializer(CustomListSerializer):
    def validate(self, attrs):
        DefinitionService.validate(attrs)
        return attrs

class DefinitionSerializer(Serializer):
    class Meta:
        model = Definition
        fields = ['content', 'knowledge_area__content']
        list_serializer_class = DefinitionListSerializer

    knowledge_area__content = StringRelatedField()
