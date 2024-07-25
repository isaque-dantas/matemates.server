from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserResponseSerializer, UserCreateSerializer


@api_view()
def hello_world(request):
    return Response("Hello, world!")


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        return Response(list(map(lambda user: UserResponseSerializer(data=user).data, User.objects.all())))

    elif request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data = serializer.data.copy()
            data.pop('password')

            serializer = UserResponseSerializer(data=data)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
