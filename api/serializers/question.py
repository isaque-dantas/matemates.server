from rest_framework import serializers

from api.models import Question
from api.serializers.custom_list_serializer import CustomListSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    # def to_representation(self, instance):
    #     return {
    #         "statement": instance.statement,
    #         "answer": instance.answer,
    #         "explanation": instance.explanation,
    #     }
