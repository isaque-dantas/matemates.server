from rest_framework.test import APIClient

import api.models
from api.models import User
from api.serializers.user import UserSerializer
from api.services.user import UserService
from api.tests import BASE_URL, base64_encoded_files
from api.tests.database_utils import DatabaseUtils
from api.tests.request_body import RequestBody
from matemates_server import settings


class UserUtils(DatabaseUtils):
    def __init__(self):
        super().__init__(User)
        self.client = APIClient()

        self.common_user_data = RequestBody.get_data("user", "common-user")
        self.admin_user_data = RequestBody.get_data("user", "admin-user")

    @property
    def common_credentials(self):
        return self.get_credentials("common-user")

    @property
    def admin_credentials(self):
        return self.get_credentials("admin-user")

    def get_credentials(self, username: str):
        if username == "admin-user":
            login_data = self.admin_user_login_data
        else:
            login_data = self.common_user_login_data

        response = self.client.post(f'{BASE_URL}/token', login_data)
        return {"Authorization": f'Bearer {response.data["access"]}'}

    @property
    def common_user_login_data(self):
        return {
            "username": self.common_user_data["username"],
            "password": self.common_user_data["password"]
        }

    @property
    def admin_user_login_data(self):
        return {
            "username": self.admin_user_data["username"],
            "password": self.admin_user_data["password"]
        }

    def get_entity_query_parameters_from_data_identifier(self, data_identifier: str):
        return {"username": data_identifier}
