import logging

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class APIViewWithAdminPermissions(APIView):
    def get_permissions(self):
        logger.debug((self.request.method, self.request.user))

        if self.request.method != 'GET':
            return [IsAdminUser()]
        return []


class APIViewWithAuthenticationRequiredExceptInPost(APIView):
    def get_permissions(self):
        logger.debug((self.request.method, self.request.user))

        if self.request.method != 'POST':
            return [IsAuthenticated()]
        return []
