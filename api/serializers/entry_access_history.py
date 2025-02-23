from rest_framework import serializers
from api.models import EntryAccessHistory
from api.services.entry import EntryService


class EntryAccessHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryAccessHistory
        fields = ['access_moment', 'entry']

    def to_representation(self, instance):
        return {
            'access_moment': instance.access_moment,
            'entry': EntryService.to_representation(instance.entry, self.context)
        }
