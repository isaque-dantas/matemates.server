from api.models import KnowledgeArea


class KnowledgeAreaService:
    @staticmethod
    def get_by_content(content: str) -> KnowledgeArea:
        return KnowledgeArea.objects.filter(content=content).first()
