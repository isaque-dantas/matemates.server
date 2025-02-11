from rest_framework import serializers

from api.models import Question
from api.serializers.custom_list_serializer import CustomListSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'statement', 'answer']
        list_serializer_class = CustomListSerializer

    def to_representation(self, instance: Question):
        representation = super().to_representation(instance)

        if isinstance(instance, Question):
            representation.update({"id": instance.pk})

        return representation