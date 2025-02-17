from rest_framework import serializers
from api.models import EntryAccessHistory


class EntryAccessHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryAccessHistory
        fields = ['access_moment', 'entry']

    def to_representation(self, instance):
        return {
            'access_moment': instance.access_moment,
            'entry_content': instance.entry.content,
        }
