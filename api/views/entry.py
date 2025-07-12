from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api import log
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api.services.entry_access_history import EntryAccessHistoryService
from api.services.knowledge_area import KnowledgeAreaService
from api.services.user import UserService
from api.views import APIViewWithAdminPermissions


class EntryView(APIViewWithAdminPermissions):
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
        serializer = EntrySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        entry = EntryService.create(serializer)
        serializer = EntrySerializer(entry)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleEntryView(APIViewWithAdminPermissions):
    @staticmethod
    def get(request, pk: int):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        entry = EntryService.get(pk)

        if (
                not UserService.can_see_non_validated_entries(request.user) and
                not entry.is_validated
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if request.user.is_authenticated:
            EntryAccessHistoryService.register(user_id=request.user.pk, entry_id=pk)

        serializer = EntrySerializer(entry, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(_, __):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def patch(request, pk):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        log.debug(request.data)

        entry = EntryService.get(pk)
        serializer = EntrySerializer(entry, data=request.data, context={'is_patch': True})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        EntryService.patch(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(_, pk: int):
        if not EntryService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        EntryService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def validate(_, pk):
    if not EntryService.exists(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    EntryService.make_entry_validated(pk)

    return Response(status=status.HTTP_204_NO_CONTENT)
