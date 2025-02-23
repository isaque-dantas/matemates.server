from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import StringRelatedField, ModelSerializer

from api import log
from api.models import Definition, Entry
from api.serializers.custom_list_serializer import CustomListSerializer
from api.services.definition import DefinitionService


class DefinitionListSerializer(CustomListSerializer):
    def validate(self, attrs):
        DefinitionService.validate(attrs)
        return attrs


class DefinitionSerializer(ModelSerializer):
    class Meta:
        model = Definition
        fields = ['id', 'content', 'knowledge_area__content', 'entry']
        list_serializer_class = DefinitionListSerializer

    knowledge_area__content = StringRelatedField()
    entry = PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Entry.objects.all())

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        log.debug(f"{internal_value=}")
        return {
            **internal_value,
            "knowledge_area__content": data.get("knowledge_area__content", None)
        }

    def validate(self, attrs):
        errors = []

        if self.context.get('is_creation') and not attrs.get("entry"):
            errors.append("É obrigatório informar o 'id' do verbete na criação da definição.")

        if not attrs.get("knowledge_area__content", None):
            errors.append("É obrigatório informar a área do conhecimento.")

        try:
            DefinitionService.validate_knowledge_area__content(attrs["knowledge_area__content"])
        except ValidationError as e:
            errors.append(e.detail)

        if errors:
            raise ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        log.debug(f"instance in DefinitionSerializer: {instance}")
        return {
            "id": instance.id,
            "content": instance.content,
            "knowledge_area": instance.knowledge_area.content,
        }
