from rest_framework.test import APIClient

from api.models import User
from api.tests import BASE_URL
from api.tests.utils.database_utils import DatabaseUtils
from api.tests.utils.request_body import RequestBody


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
