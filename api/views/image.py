from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.image import ImageService


class ImageView(APIView):
    @staticmethod
    def get(request, pk):
        if not ImageService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        image = ImageService.get(pk)
        return FileResponse(image.content.open(), status=status.HTTP_200_OK)
