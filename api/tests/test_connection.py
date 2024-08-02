from rest_framework.test import APITestCase
from rest_framework import status
from ..tests import BASE_URL


class ConnectionTests(APITestCase):
    def test_connection__should_return_OK(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
