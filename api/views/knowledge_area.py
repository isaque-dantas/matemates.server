from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import KnowledgeArea
from api.serializers.knowledge_area import KnowledgeAreaSerializer


class KnowledgeAreaView(APIView):
    @staticmethod
    def get(request):
        knowledge_areas = KnowledgeArea.objects.all()
        serializer = KnowledgeAreaSerializer(
            knowledge_areas,
            many=True,
            context={
                'is_knowledge_area_get': True,
                'is_user_staff': request.user and request.user.is_staff
            }
        )

        return Response(serializer.data)
