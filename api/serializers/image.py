from rest_framework import serializers

from api.models import Image
from api.serializers.custom_list_serializer import CustomListSerializer
from drf_base64.fields import Base64ImageField

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['caption', 'base64_image', 'format']
        list_serializer_class = CustomListSerializer

    base64_image = Base64ImageField(source='content')
    caption = serializers.CharField(required=False)
    format = serializers.CharField()

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "caption": instance.caption,
        }

    def __repr__(self):
        return self.caption

    def __str__(self):
        return self.caption
