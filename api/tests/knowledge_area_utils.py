from api.models.knowledge_area import KnowledgeArea


class KnowledgeAreaUtils:
    knowledge_areas = [
        {"content": "estatística", "subject": "matemática"},
        {"content": "álgebra", "subject": "matemática"},
        {"content": "cálculo", "subject": "matemática"},
        {"content": "cinemática", "subject": "física"},
    ]

    @staticmethod
    def create_all():
        for knowledge_area in KnowledgeAreaUtils.knowledge_areas:
            if not KnowledgeAreaUtils.exists(knowledge_area['content']):
                area = KnowledgeArea(**knowledge_area)
                area.save()

    @staticmethod
    def exists(content: str):
        return KnowledgeArea.objects.filter(content=content).exists()
