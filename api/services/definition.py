from api.models import Definition
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
