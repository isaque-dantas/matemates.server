from rest_framework import serializers

from api.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data)
        return instance
