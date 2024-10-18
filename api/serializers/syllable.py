from rest_framework.serializers import Serializer

import api.models


class SyllableSerializer(Serializer):
    class Meta:
        model = api.models.Syllable
        fields = '__all__'

    def save_syllables(self, term, term_content: str):
        syllables_data = self.Meta.model.objects.get_syllables_data(term, term_content)
        for syllable_data in syllables_data:
            self.Meta.model.objects.create(syllable_data)
