from rest_framework.serializers import Serializer

from api.models import Question
from api.serializers.custom_list_serializer import CustomListSerializer


class QuestionSerializer(Serializer):
    class Meta:
        model = Question
        fields = ['statement', 'answer', 'explanation']
        list_serializer_class = CustomListSerializer
