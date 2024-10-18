from rest_framework.serializers import Serializer, StringRelatedField, RelatedField

from api.models import Definition
from api.serializers.custom_list_serializer import CustomListSerializer


class DefinitionSerializer(Serializer):
    class Meta:
        model = Definition
        fields = ['content', 'knowledge_area__content']
        list_serializer_class = CustomListSerializer

    knowledge_area__content = StringRelatedField()
