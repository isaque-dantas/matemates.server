from rest_framework.serializers import Serializer

import api.models


class SyllableSerializer(Serializer):
    class Meta:
        model = api.models.Syllable
        fields = '__all__'

    def create(self, validated_data):
        terms_contents = self.get_terms_contents_from_content(validated_data['content'])
        terms = self.get_terms
        for i, syllable_content in enumerate(term_content.split(".")):
            syllable_data = dict()
            syllable_data.update({"content": self.parse_content(syllable_content)})
            syllable_data.update({"order": i})

            syllable = api.models.Syllable(**syllable_data)
            syllable.term = term
            syllable.save()

    @staticmethod
    def get_terms_contents_from_content(content):
        return content.replace("*", "").split()
