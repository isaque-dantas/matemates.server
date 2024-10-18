from rest_framework import serializers

from api.models import Image
from api.serializers.custom_list_serializer import CustomListSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['caption', 'base64_encoded_string', 'path']
        list_serializer_class = CustomListSerializer

    base64_encoded_string = serializers.CharField()
    path = serializers.CharField(required=False)

    def validate(self, attrs):
        return attrs
