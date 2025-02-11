from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.image import ImageService
from api.services.user import UserService


class ImageView(APIView):
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
        return FileResponse(image.content.open(), status=status.HTTP_200_OK)

@api_view()
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