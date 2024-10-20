from rest_framework import serializers

from api.models import KnowledgeArea


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = '__all__'
