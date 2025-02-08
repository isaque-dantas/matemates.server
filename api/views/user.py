from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from api import log
from api.serializers.user import UserSerializer
from api.services.user import UserService


@api_view()
def hello_world(request):
    return Response("Hello, world!")


@api_view(['POST'])
def turn_admin_view(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)

    user_who_invited = request.user
    UserService.turn_admin(request.data['email'], user_who_invited)
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

        user = UserService.create(serializer)
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

        UserService.inactivate_user(request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)
