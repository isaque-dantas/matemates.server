from rest_framework.serializers import Serializer

from api.models import Question


class QuestionSerializer(Serializer):
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        pass
