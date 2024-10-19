from rest_framework.exceptions import ValidationError

from api.models import Definition, KnowledgeArea
from api.services.knowledge_area import KnowledgeAreaService

from api import log
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
            [DefinitionService.create(data, entry) for data in data_list]
        )

    @staticmethod
    def create(data, entry):
        log.debug(f"{data['knowledge_area']=}")
        return Definition(content=data["content"], entry=entry, knowledge_area=data["knowledge_area"])

    @staticmethod
    def does_knowledge_area_content_exist(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()

    @staticmethod
    def validate(attrs):
        errors = []

        for attr in attrs:
            try:
                DefinitionService.validate_knowledge_area__content(
                    attr["knowledge_area__content"]
                )
            except ValidationError as err:
                errors.append({"knowledge_area__content": err.detail})
            else:
                errors.append({})

        log.debug(f'{errors=}')

        if errors:
            raise ValidationError({'definitions': errors})

    @staticmethod
    def validate_knowledge_area__content(value):
        if not DefinitionService.does_knowledge_area_content_exist(value):
            raise ValidationError(f"KnowledgeArea content '{value}' does not exist in database")

