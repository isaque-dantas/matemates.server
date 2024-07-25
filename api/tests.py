from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Create your tests here.

BASE_URL = "http://127.0.0.1:8000/api"


class ConnectionTests(APITestCase):
    def test_connection(self):
        response = self.client.get(f'{BASE_URL}/hello-world')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
