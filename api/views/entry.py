import logging

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Entry
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api import log

class EntryView(APIView):
    @staticmethod
    def get(request):
        if request.query_params and "knowledge_area" in request.query_params:
            entries = EntryService.get_all_related_to_knowledge_area(
                request.query_params["knowledge_area"]
            )
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

        print('\n----------------\n\n'*3)
        print("in SingleEntryView.get\n")

        entry = EntryService.get(pk)
        serializer = EntrySerializer(entry)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        raise NotImplementedError()

    def delete(self, request):
        raise NotImplementedError()
