from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import KnowledgeArea
from api.serializers.knowledge_area import KnowledgeAreaSerializer


class KnowledgeAreaView(APIView):
    @staticmethod
    def get(request):
        knowledge_areas = KnowledgeArea.objects.all()
        serializer = KnowledgeAreaSerializer(knowledge_areas, many=True)

        return Response(serializer.data)
