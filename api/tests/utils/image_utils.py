from api.models import Image
from api.tests.utils.database_utils import DatabaseUtils


class ImageUtils(DatabaseUtils):
    def __init__(self):
        super().__init__(Image)

    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str | int) -> dict:
        if isinstance(data_identifier, int):
            question_pk = data_identifier
        else:
            question_pk = self.get_pk_from_data_identifier(data_identifier)

        return {"pk": question_pk}

    @staticmethod
    def get_pk_from_data_identifier(data_identifier: str) -> int:
        entry_content, question_order = data_identifier.split("-")
        question = (
            Image.objects
            .filter(entry__content=entry_content)
            .values("pk")
            [int(question_order)]
        )
        return question["pk"]