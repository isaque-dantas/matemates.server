from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@api_view()
def hello_world(request):
    return Response("Hello, world!")


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        return Response(list(map(lambda user: UserSerializer(data=user).data, User.objects.all())))
    elif request.method == 'POST':
        data = request.data.copy()
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
