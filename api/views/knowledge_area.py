from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import KnowledgeArea
from api.serializers.knowledge_area import KnowledgeAreaSerializer
from api.services.knowledge_area import KnowledgeAreaService
from api.services.user import UserService


class KnowledgeAreaView(APIView):
    @staticmethod
    def get(request):
        knowledge_areas = KnowledgeArea.objects.all()
        serializer = KnowledgeAreaSerializer(
            knowledge_areas,
            many=True,
            context={
                'is_knowledge_area_get': True,
                'should_get_only_validated': UserService.can_see_non_validated_entries(request.user)
            }
        )

        return Response(serializer.data)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = KnowledgeAreaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        knowledge_area = KnowledgeAreaService.create(serializer)
        serializer = KnowledgeAreaSerializer(knowledge_area)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleKnowledgeAreaView(APIView):
    @staticmethod
    def get(request, pk):
        if not KnowledgeAreaService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        knowledge_area = KnowledgeAreaService.get(pk)
        serializer = KnowledgeAreaSerializer(
            knowledge_area,
            context={
                'is_knowledge_area_get': True,
                'should_get_only_validated': UserService.can_see_non_validated_entries(request.user)
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk):
        if not KnowledgeAreaService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        knowledge_area_to_update = KnowledgeAreaService.get(pk)
        serializer = KnowledgeAreaSerializer(
            instance=knowledge_area_to_update,
            data=request.data
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        KnowledgeAreaService.update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod

    def delete(request, pk):
        if not KnowledgeAreaService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        KnowledgeAreaService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)