from rest_framework.serializers import Serializer

import api.models


class SyllableSerializer(Serializer):
    class Meta:
        model = api.models.Syllable
        fields = '__all__'

    def to_representation(self, instance):
        return instance.content
