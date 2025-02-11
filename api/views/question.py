from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class QuestionView(APIView):
    @staticmethod
    def post():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SingleQuestionView(APIView):
    @staticmethod
    def get():
        pass