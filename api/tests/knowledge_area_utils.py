from api.models.knowledge_area import KnowledgeArea
from api.serializers.knowledge_area import KnowledgeAreaSerializer
from api.services.knowledge_area import KnowledgeAreaService


class KnowledgeAreaUtils:
    knowledge_areas = {
        "estatistica": {"content": "estatística", "subject": "matemática"},
        "algebra": {"content": "álgebra", "subject": "matemática"},
        "calculo": {"content": "cálculo", "subject": "matemática"},
        "cinematica": {"content": "cinemática", "subject": "física"},
    }

    @staticmethod
    def create_all():
        for key in KnowledgeAreaUtils.knowledge_areas:
            data = KnowledgeAreaUtils.knowledge_areas[key]

            if not KnowledgeAreaUtils.exists(data["content"]):
                area = KnowledgeArea(**data)
                area.save()

    @staticmethod
    def exists(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()

    @staticmethod
    def get(pk: int):
        return KnowledgeArea.objects.get(pk=pk)

    def set_database_environment(self, environment: dict[str, bool]):
        environment = environment or {key: False for key in KnowledgeAreaUtils.knowledge_areas}
        actions = {
            True: lambda e: self.create(e),
            False: lambda e: self.delete(e),
        }

        KnowledgeAreaUtils.create_all()

        for content, must_create in environment.items():
            actions[must_create](content)

    @staticmethod
    def retrieve(content: str):
        return KnowledgeArea.objects.get(content=content)

    def create(self, content: str):
        if self.exists(content):
            return None

        serializer = KnowledgeAreaSerializer(data=self.get_data(content))
        serializer.is_valid(raise_exception=True)
        KnowledgeAreaService.create(serializer)

    def delete(self, content: str):
        if not self.exists(content):
            return None

        KnowledgeArea.objects.filter(content=content).delete()

    @staticmethod
    def get_data(data_identifier: str):
        data = KnowledgeAreaUtils.knowledge_areas[data_identifier].copy()
        copied_data = {}
        for key in data:
            if data[key] is list:
                copied_data[key] = [dict_in_list.copy() for dict_in_list in data[key]]
            else:
                copied_data[key] = data[key]

        return copied_data
