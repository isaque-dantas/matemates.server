from rest_framework import serializers
from api.models import EntryAccessHistory, Entry
from api.services.entry import EntryService


class EntryAccessHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryAccessHistory
        fields = ['access_moment', 'entry']

    def to_representation(self, instance):
        print(isinstance(instance, Entry))
        print(isinstance(instance, EntryAccessHistory))
        print(type(instance))

        if isinstance(instance, Entry):
            return {
                'access_moment': instance.access_moment,
                'entry': EntryService.to_representation(instance, self.context)
            }
        elif isinstance(instance, EntryAccessHistory):
            return {
                'access_moment': instance.access_moment,
                'entry': EntryService.to_representation(instance.entry, self.context)
            }
