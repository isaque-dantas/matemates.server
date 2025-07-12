import django.db.models
from rest_framework.exceptions import ValidationError

from api import log
from api.models import Definition, KnowledgeArea, Entry
from api.services.knowledge_area import KnowledgeAreaService


class DefinitionService:
    @staticmethod
    def create_all(entry_data, entry):
        data_list = [
            {
                'content': definition_data['content'],
                'knowledge_area':
                    KnowledgeAreaService.get_by_content(definition_data["knowledge_area__content"])
            }

            for definition_data in entry_data["definitions"]
        ]

        return Definition.objects.create(
            [DefinitionService.get_instance_from_data(data, entry) for data in data_list]
        )

    @staticmethod
    def get_instance_from_data(data, entry):
        # log.debug(f"{data['knowledge_area']=}")
        return Definition(content=data["content"], entry=entry, knowledge_area=data["knowledge_area"])

    @staticmethod
    def does_knowledge_area_content_exist(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()

    @staticmethod
    def validate(data):
        errors = []

        for attr in data:
            try:
                DefinitionService.validate_knowledge_area__content(
                    attr["knowledge_area__content"]
                )
            except ValidationError as err:
                errors.append({"knowledge_area__content": err.detail})
            else:
                errors.append({})

        if errors and list(filter(lambda error: error != {}, errors)) != []:
            raise ValidationError({'definitions': errors})

    @staticmethod
    def validate_knowledge_area__content(value):
        if not DefinitionService.does_knowledge_area_content_exist(value):
            raise ValidationError(f"KnowledgeArea content '{value}' does not exist in database")

    @staticmethod
    def exists(pk):
        return Definition.objects.filter(pk=pk).exists()

    @staticmethod
    def get(pk):
        return Definition.objects.get(pk=pk)

    @staticmethod
    def is_parent_validated(pk):
        return DefinitionService.get(pk).entry.is_validated

    @staticmethod
    def update(serializer):
        instance: django.db.models.Model = serializer.instance
        data = serializer.validated_data

        log.debug(f"{data=}")
        log.debug(f"{serializer.data=}")
        log.debug(f"{serializer.initial_data=}")
        log.debug(f"{serializer.errors=}")
        log.debug(f"{instance=}")

        instance.content = data["content"]
        instance.knowledge_area = KnowledgeAreaService.get_by_content(data["knowledge_area__content"])
        instance.save()

    @staticmethod
    def delete(pk):
        Definition.objects.filter(pk=pk).delete()

    @classmethod
    def create(cls, serializer):
        data = serializer.validated_data

        knowledge_area = KnowledgeAreaService.get_by_content(data["knowledge_area__content"])
        data.update({"knowledge_area": knowledge_area})

        definition = cls.get_instance_from_data(data, data["entry"])
        definition.save()

        return definition
