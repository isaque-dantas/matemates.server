from rest_framework.serializers import Serializer

from api.models import Term


class TermSerializer(Serializer):
    class Meta:
        model = Term
        fields = '__all__'

    def create(self, validated_data):
        pass
