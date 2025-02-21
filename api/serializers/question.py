from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from api.models import Question, Entry
from api.serializers.custom_list_serializer import CustomListSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'statement', 'answer', 'entry']
        list_serializer_class = CustomListSerializer

    entry = PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Entry.objects.all())

    def to_representation(self, instance: Question):
        representation = super().to_representation(instance)

        if isinstance(instance, Question):
            representation.update({"id": instance.pk})

        return representation

    def validate(self, attrs):
        errors = []

        if self.context.get('is_creation') and not attrs.get("entry"):
            errors.append({"entry": "É obrigatório informar o 'id' do verbete na criação do exemplo."})

        if errors:
            raise ValidationError(errors)

        return attrs