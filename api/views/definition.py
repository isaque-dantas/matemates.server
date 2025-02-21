from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import log
from api.serializers.definition import DefinitionSerializer
from api.services.definition import DefinitionService
from api.services.knowledge_area import KnowledgeAreaService
from api.services.user import UserService


class DefinitionView(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = DefinitionSerializer(data=request.data, context={'is_creation': True})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        definition = DefinitionService.create(serializer)
        serializer = DefinitionSerializer(definition)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleDefinitionView(APIView):
    @staticmethod
    def get(request, pk: int):
        if not DefinitionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        log.debug(f"{UserService.can_see_non_validated_entries(request.user)=}")
        log.debug(f"{DefinitionService.is_parent_validated(pk)=}")

        if (
                not UserService.can_see_non_validated_entries(request.user) and
                not DefinitionService.is_parent_validated(pk)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        definition = DefinitionService.get(pk)
        serializer = DefinitionSerializer(definition)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk):
        if not DefinitionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        definition_to_update = DefinitionService.get(pk)
        serializer = DefinitionSerializer(instance=definition_to_update, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        DefinitionService.update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not DefinitionService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        DefinitionService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
