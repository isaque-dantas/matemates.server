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

    def set_database_environment(self, environment: dict[str, bool] = None):
        environment = environment or {'common-user': False, 'admin-user': False}
        actions = {
            True: lambda u: self._create_user_if_doesnt_exist(u),
            False: lambda u: self._delete_user_if_exists(u),
        }

        self.refresh_tokens()

        for username, must_create in environment.items():
            actions[must_create](username)

    def retrieve_user(self, username: str = None) -> User:
        username = username or self.common_user_data["username"]
        return User.objects.get(username=username)

    def _does_user_exist(self, username: str = None) -> bool:
        username = username or self.common_user_data["username"]
        return User.objects.filter(username=username).exists()

    def _create_user_if_doesnt_exist(self, username: str):
        if self._does_user_exist(username):
            return None

        serializer = UserSerializer(data=self._users_data[username])
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

    def _delete_user_if_exists(self, username: str):
        if not self._does_user_exist(username):
            return None

        user = self.retrieve_user(username)
        user.delete()

    @property
    def common_credentials(self):
        return self.get_credentials(self.common_user_data['username'])

    @property
    def admin_credentials(self):
        return self.get_credentials(self.admin_user_data['username'])

    def get_credentials(self, username: str):
        if self._credentials_headers[username]:
            return self._credentials_headers[username]

        login_data = self.common_user_login_data if username == 'common-user' else self.admin_user_login_data
        response = self.client.post(f'{BASE_URL}/token', login_data)

        self._credentials_headers[username] = {"Authorization": f'Bearer {response.data["access"]}'}
        return self._credentials_headers[username]

    def refresh_tokens(self):
        self._credentials_headers['admin-user'] = None
        self._credentials_headers['common-user'] = None

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
