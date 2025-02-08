from api.models.knowledge_area import KnowledgeArea
from api.tests.database_utils import DatabaseUtils
from api.tests.request_body import RequestBody


class KnowledgeAreaUtils(DatabaseUtils):
    def __init__(self):
        super().__init__(KnowledgeArea)

    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str):
        content = RequestBody.get_data("knowledge_area", data_identifier)["content"]
        return {"content": content}
