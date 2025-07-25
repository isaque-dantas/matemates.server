from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.entry import EntrySerializer
from api.serializers.entry_access_history import EntryAccessHistorySerializer
from api.services.entry_access_history import EntryAccessHistoryService
from api.services.user import UserService


class EntryAccessHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        history = EntryAccessHistoryService.get_from_user(request.user.pk)
        serializer = EntryAccessHistorySerializer(history, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_most_accessed_entries(request):
    entries = EntryAccessHistoryService.get_most_accessed(
        not UserService.can_see_non_validated_entries(request.user)
    )

    serializer = EntrySerializer(entries, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
