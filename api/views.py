from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.serializers import UserSerializer, UserUpdateSerializer


@api_view()
def hello_world(request):
    return Response("Hello, world!")


class UserView(APIView):
    @action(detail=True)
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def put(self, request):
        if request.user.is_authenticated:
            serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            serializer.inactivate_user(request.user.username)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
