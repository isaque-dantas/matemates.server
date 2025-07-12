from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import log

from api.models import Image, Entry
from api.serializers.custom_list_serializer import CustomListSerializer
from drf_base64.fields import Base64ImageField

from api.services.image import ImageService


class ImageListSerializer(CustomListSerializer):
    def validate(self, attrs):
        log.debug("PASSOU EM IMAGELISTSERIALIZER")
        ImageService.validate(attrs)
        return attrs


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['caption', 'base64_image', 'id', 'entry']
        list_serializer_class = ImageListSerializer

    id = serializers.IntegerField(read_only=True, required=False)
    base64_image = Base64ImageField(source='content', required=False)
    caption = serializers.CharField(required=False)
    entry = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Entry.objects.all())

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

    def validate(self, attrs):
        errors = []

        log.debug("PASSOU EM IMAGESERIALIZER VALIDATE")

        if not self.context.get('is_update') and 'content' not in attrs:
            errors.append('O conteúdo da imagem é obrigatório.')

        if self.context.get('is_creation') and not attrs.get("entry"):
            errors.append("É obrigatório informar o 'id' do verbete na criação da imagem.")

        if not ImageService.is_content_base64_encoded(attrs.get('base64_image')):
            errors.append("A imagem deve estar no formato base64.")

        if errors:
            raise ValidationError(errors)

        return attrs

    def __repr__(self):
        return self.caption

    def __str__(self):
        return self.caption
