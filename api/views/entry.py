from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.entry import EntrySerializer


class EntryView(APIView):
    def get(self, request):
        raise NotImplementedError()

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status.HTTP_401_UNAUTHORIZED)
        elif not request.user.is_admin:
            return Response(status.HTTP_403_FORBIDDEN)
        print(request.data.dict())
        serializer = EntrySerializer(data=request.data.dict())

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.create(serializer.initial_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        raise NotImplementedError()

    def delete(self, request):
        raise NotImplementedError()
