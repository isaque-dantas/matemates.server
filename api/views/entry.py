import logging

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api import log

class EntryView(APIView):
    def get(self, request):
        raise NotImplementedError()

    # @permission_classes([IsAdminUser])
    def post(self, request):
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

    def put(self, request):
        raise NotImplementedError()

    def delete(self, request):
        raise NotImplementedError()
