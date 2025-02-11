from api.tests.utils.database_utils import DatabaseUtils
from api.models.definition import Definition


class DefinitionUtils(DatabaseUtils):
    def __init__(self):
        super().__init__(Definition)

    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str | int) -> dict:
        if isinstance(data_identifier, int):
            definition_pk = data_identifier
        else:
            definition_pk = self.get_pk_from_data_identifier(data_identifier)

        return {"pk": definition_pk}

    @staticmethod
    def get_pk_from_data_identifier(data_identifier: str) -> int:
        entry_content, definition_order = data_identifier.split("-")
        definition = (
            Definition.objects
            .filter(entry__content=entry_content)
            .values("pk")
            [int(definition_order)]
        )
        return definition["pk"]
