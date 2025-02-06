from rest_framework import serializers

from api import log
from api.models import KnowledgeArea
from api.services.entry import EntryService
from api.services.knowledge_area import KnowledgeAreaService


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get('is_knowledge_area_get'):
            should_get_only_validated_entries: bool = self.context.get('is_user_staff')

            related_entries = EntryService.get_all_related_to_knowledge_area(
                knowledge_area_content=instance.content,
                should_get_only_validated=should_get_only_validated_entries
            )
            representation["entries"] = EntryService.get_data_from_instances(related_entries)

            log.debug(f"{instance.content=}")
            log.debug(f"{related_entries=}")
            log.debug(f"{representation['entries']=}")

        return representation

    def validate_content(self, content: str) -> str:
        instance = self.instance

        errors = KnowledgeAreaService.get_validation_errors_in_content(content, instance=instance)
        if errors:
            raise serializers.ValidationError(errors)

        return content
