from rest_framework import serializers

from api import log
from api.models import KnowledgeArea
from api.services.entry import EntryService


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'is_knowledge_area_get' in self.context and self.context['is_knowledge_area_get'] == True:
            related_entries = EntryService.get_all_related_to_knowledge_area(knowledge_area_content=instance.content)
            representation["entries"] = EntryService.get_data_from_instances(related_entries)

            log.debug(f"{instance.content=}")
            log.debug(f"{related_entries=}")
            log.debug(f"{representation['entries']=}")

        return representation
