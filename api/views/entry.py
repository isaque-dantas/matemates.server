from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import log
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api.services.knowledge_area import KnowledgeAreaService
from api.services.user import UserService


class EntryView(APIView):
    @staticmethod
    def get(request):
        should_get_only_validated = not UserService.can_see_non_validated_entries(request.user)
        log.debug(f'{should_get_only_validated=}')

        if request.query_params and "knowledge_area" in request.query_params:
            knowledge_area__content = request.query_params["knowledge_area"]

            if not KnowledgeAreaService.exists_content(knowledge_area__content):
                return Response(status=status.HTTP_404_NOT_FOUND)

            entries = EntryService.get_all_related_to_knowledge_area(knowledge_area__content, should_get_only_validated)
        elif request.query_params and "search_query" in request.query_params:
            search_query = request.query_params["search_query"]
            entries = EntryService.search_by_content(search_query, should_get_only_validated)

            # all_entries = EntryService.get_all(should_get_only_validated)
            # log.debug(f'{entries=}')
            # log.debug(f'{[entry.content for entry in all_entries]=}')
            # log.debug(f'{search_query=}')
            # log.debug(f'{should_get_only_validated=}')
        else:
            entries = EntryService.get_all(should_get_only_validated)

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

        entry = EntryService.get(pk)
        serializer = EntrySerializer(entry, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def patch(request, pk):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if "content" not in request.data:
            return Response({"content": "Este campo é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EntrySerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        entry = EntryService.get(pk)
        EntryService.patch_content(instance=entry, content=serializer.data["content"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        EntryService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def validate(request, pk):
    if not EntryService.exists(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)

    EntryService.make_entry_validated(pk)

    return Response(status=status.HTTP_204_NO_CONTENT)
