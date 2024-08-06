from rest_framework.serializers import Serializer

import api.models
from api.serializers.syllable import SyllableSerializer


class TermSerializer(Serializer):
    class Meta:
        model = api.models.Term
        fields = '__all__'

    def create(self, validated_data):
        self.Meta.model.objects.create(**validated_data)
