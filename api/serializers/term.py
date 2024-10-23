from rest_framework import serializers

import api.models
from api import log
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.syllable import SyllableSerializer
from api.services.syllable import SyllableService


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Term
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def to_representation(self, instance):
        syllables_data = SyllableService.get_data_related_to_term(instance)

        return {
            "id": instance.id,
            "content": instance.content,
            "gender": instance.gender,
            "grammatical_category": instance.grammatical_category,
            "is_main_term": instance.is_main_term,
            "syllables": syllables_data,
        }
