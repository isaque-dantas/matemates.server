from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user import UserSerializer, UserUpdateSerializer
from api.services.entry import EntryService
from api.services.user import UserService
from api import log

@api_view()
def hello_world(request):
    return Response("Hello, world!")


@api_view(['POST'])
def turn_admin(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not request.user.is_admin:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(request.user)
    serializer.turn_admin(request.data['email'])
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    @action(detail=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            log.error(f"{serializer.errors=}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.create(serializer.validated_data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT'])
    def put(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        UserService.update(request.user, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        serializer.inactivate_user(request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)
