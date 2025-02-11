from rest_framework import serializers

from api.models import Question
from api.serializers.custom_list_serializer import CustomListSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'statement', 'answer']
        list_serializer_class = CustomListSerializer

    def to_representation(self, instance: Question):
        return {
            "id": instance.pk,
            "statement": instance.statement,
            "answer": instance.answer,
        }