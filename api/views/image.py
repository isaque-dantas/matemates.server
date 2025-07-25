from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from api.serializers.image import ImageSerializer
from api.services.image import ImageService
from api.services.user import UserService
from api.views import APIViewWithAdminPermissions


class ImageView(APIViewWithAdminPermissions):
    @staticmethod
    def post(request):
        serializer = ImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = ImageService.create(serializer)
        serializer = ImageSerializer(image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleImageView(APIView):
    @staticmethod
    def get(request, pk):
        if not ImageService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (
                not UserService.can_see_non_validated_entries(request.user) and
                not ImageService.is_parent_validated(pk)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        image = ImageService.get(pk)
        serializer = ImageSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk):
        if not ImageService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        image = ImageService.get(pk)
        serializer = ImageSerializer(image, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ImageService.update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(_, pk):
        if not ImageService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        ImageService.delete(pk)
        return Response(status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_image_blob_file(request, pk):
    if not ImageService.exists(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if (
            not UserService.can_see_non_validated_entries(request.user) and
            not ImageService.is_parent_validated(pk)
    ):
        return Response(status=status.HTTP_403_FORBIDDEN)

    image = ImageService.get(pk)
    return FileResponse(image.content.open(), status=status.HTTP_200_OK)
