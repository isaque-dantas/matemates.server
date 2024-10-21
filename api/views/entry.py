from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import log
from api.models import Entry
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api.services.knowledge_area import KnowledgeAreaService


class EntryView(APIView):
    @staticmethod
    def get(request):
        if request.query_params and "knowledge_area" in request.query_params:
            knowledge_area__content = request.query_params["knowledge_area"]

            if not KnowledgeAreaService.exists_content(knowledge_area__content):
                return Response(status=status.HTTP_404_NOT_FOUND)

            entries = EntryService.get_all_related_to_knowledge_area(knowledge_area__content)
        else:
            entries = EntryService.get_all()

        serializer = EntrySerializer(entries, many=True)

        return Response(serializer.data)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        log.debug(f'{request.user.is_staff=}')

        serializer = EntrySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        entry = EntryService.create(serializer)
        serializer = EntrySerializer(entry)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleEntryView(APIView):
    @staticmethod
    def get(request, pk: int):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        print('\n----------------\n\n' * 3)
        print("in SingleEntryView.get\n")

        entry = EntryService.get(pk)
        serializer = EntrySerializer(entry)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        entry_to_update = EntryService.get(pk)
        serializer = EntrySerializer(instance=entry_to_update, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        EntryService.update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        EntryService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
