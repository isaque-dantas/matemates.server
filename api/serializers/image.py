from django.urls import reverse
from rest_framework import serializers

from api.models import Image
from api.serializers.custom_list_serializer import CustomListSerializer
from drf_base64.fields import Base64ImageField

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['caption', 'base64_image', 'id']
        list_serializer_class = CustomListSerializer

    id = serializers.IntegerField(read_only=True, required=False)
    base64_image = Base64ImageField(source='content')
    caption = serializers.CharField(required=False)

    def to_representation(self, instance):
        return {
            "caption": instance.caption,
            "url": self.get_url(instance.id),
            "id": instance.id
        }

    def get_url(self, image_pk):
        relative_url = reverse('entry-image-blob-file', kwargs={'pk': image_pk})

        if self.context:
            return self.context.get('request').build_absolute_uri(relative_url)

        return relative_url

    def __repr__(self):
        return self.caption

    def __str__(self):
        return self.caption
