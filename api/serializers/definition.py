from rest_framework.serializers import Serializer

from api.models import Definition


class DefinitionSerializer(Serializer):
    class Meta:
        model = Definition
        fields = '__all__'

    def create(self, validated_data):
        pass
