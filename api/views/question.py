from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Question
from api.serializers.question import QuestionSerializer
from api.services.definition import DefinitionService
from api.services.question import QuestionService
from api.services.user import UserService
from api import log

class QuestionView(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = QuestionSerializer(data=request.data, context={'is_creation': True})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        question = QuestionService.create(serializer)
        serializer = QuestionSerializer(question)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SingleQuestionView(APIView):
    @staticmethod
    def get(request, pk):
        if not QuestionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (
                not UserService.can_see_non_validated_entries(request.user) and
                not QuestionService.is_parent_validated(pk)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        question = QuestionService.get(pk)
        serializer = QuestionSerializer(question)

        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        if not QuestionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        question_to_update = QuestionService.get(pk)
        serializer = QuestionSerializer(instance=question_to_update, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        QuestionService.update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk):
        if not QuestionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        QuestionService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
