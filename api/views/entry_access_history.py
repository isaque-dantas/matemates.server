from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.entry_access_history import EntryAccessHistorySerializer
from api.services.entry_access_history import EntryAccessHistoryService


class EntryAccessHistoryView(APIView):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        history = EntryAccessHistoryService.get_from_user(request.user.pk)
        serializer = EntryAccessHistorySerializer(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
