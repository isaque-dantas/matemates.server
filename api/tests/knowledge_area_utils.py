from api.models.knowledge_area import KnowledgeArea


class KnowledgeAreaUtils:
    knowledge_areas = [
        {"content": "estatística", "subject": "matemática"},
        {"content": "álgebra", "subject": "matemática"},
        {"content": "cálculo", "subject": "matemática"},
        {"content": "cinemática", "subject": "física"},
    ]

    def __init__(self):
        self.create_all()

    def create_all(self):
        print("create_all from knowledge_areas")
        for knowledge_area in self.knowledge_areas:
            if not self.exists(knowledge_area['content']):
                KnowledgeArea.objects.create(**knowledge_area)

    @staticmethod
    def exists(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()
