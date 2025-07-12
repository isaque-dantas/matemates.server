from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import log
from api.serializers.user import UserSerializer
from api.services.user import UserService
from api.views import APIViewWithAuthenticationRequiredExceptInPost


@api_view(['POST'])
@permission_classes([IsAdminUser])
def turn_admin_view(request):
    user_who_invited = request.user
    UserService.turn_admin(request.data['email'], user_who_invited)
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIViewWithAuthenticationRequiredExceptInPost):
    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            log.error(f"{serializer.errors=}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.create(serializer)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request):
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={"is_update": True})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        UserService.update(request.user, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request):
        UserService.inactivate_user(request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def patch(request):
        serializer = UserSerializer(request.user, data=request.data, context={'is_profile_image_update': True})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        UserService.update_profile_image(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get(request):
        return FileResponse(request.user.profile_image, status=status.HTTP_200_OK)
