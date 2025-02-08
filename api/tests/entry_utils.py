from api.models.entry import Entry
from api.tests.database_utils import DatabaseUtils
from api.tests.knowledge_area_utils import KnowledgeAreaUtils


class EntryUtils(DatabaseUtils):
    def __init__(self):
        super().__init__(Entry)
        KnowledgeAreaUtils().create_all()

    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str):
        parsed_identifier = (
            data_identifier
            .replace("*", "")
            .replace(".", "")
        )

        return {"content": parsed_identifier}
