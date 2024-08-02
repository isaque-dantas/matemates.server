from rest_framework.test import APIClient
from matemates_server import settings
from api.models import User
from ..serializers.user import UserSerializer
from ..tests import BASE_URL


class UserTestsUtils:
    def __init__(self):
        self.client = APIClient()

    common_user_data = {
        "first_name": "Common",
        "last_name": "User",
        "email": "common-user@email.com",
        "password": "pass",
        "username": "common-user"
    }

    admin_user_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": settings.ADMIN_EMAIL,
        "password": "pass",
        "username": "admin-user"
    }

    _credentials_headers = {
        admin_user_data['username']: None,
        common_user_data['username']: None
    }

    _users_data = {
        admin_user_data['username']: admin_user_data,
        common_user_data['username']: common_user_data
    }

    @property
    def common_credentials(self):
        return self.get_credentials(self.common_user_data['username'])

    @property
    def admin_credentials(self):
        return self.get_credentials(self.admin_user_data['username'])

    def get_credentials(self, username: str):
        user_data = self._users_data[username]

        if self._credentials_headers[username]:
            return self._credentials_headers[username]

        if not self.does_user_exist(username):
            self.create_user(user_data)

        response = self.client.post(f'{BASE_URL}/token', user_data)

        self._credentials_headers[username] = {"Authorization": f'Bearer {response.data["access"]}'}
        return self._credentials_headers[username]

    @property
    def common_user_login_data(self):
        return {
            "username": self.common_user_data["username"],
            "password": self.common_user_data["password"]
        }

    def retrieve_user(self, username: str = None) -> User:
        username = username or self.common_user_data["username"]
        return User.objects.get(username=username)

    def does_user_exist(self, username: str = None) -> bool:
        username = username or self.common_user_data["username"]
        return User.objects.filter(username=username).exists()

    def create_user(self, data: dict = None):
        if self.does_user_exist(data['username']):
            return None

        data = data or self.common_user_data

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        self._credentials_headers[data['username']] = None

    def delete_user(self, username: str = None):
        if not self.does_user_exist(username):
            return None

        user = self.retrieve_user(username)
        user.delete()

        self._credentials_headers[username] = None
