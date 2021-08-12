from django.core.cache import cache
from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.test import APITestCase

from account.models import User


class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='foo@example.com', username='foo', password='Aa123456!')
        jwt_creation_url = 'http://127.0.0.1:8000/auth/jwt/create'
        user_data = {'email': self.user.email, 'password': 'Aa123456!'}
        response = self.client.post(jwt_creation_url, user_data, format='json')
        self.token = response.data['access']

    def test_user_register(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        user_credentials = {'username': 'admin', 'email': 'admin@example.com', 'password': 'Aa123456!'}
        response = self.client.post(url, user_credentials)
        expected_data = {'username': 'admin', 'email': 'admin@example.com', 'id': 2}
        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_user_login(self):
        url = 'http://127.0.0.1:8000/auth/jwt/create'
        user_data = {'email': self.user.email, 'password': 'Aa123456!'}
        response = self.client.post(url, user_data, format='json')
        token = response.data['access']
        token_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.id, int(token_data['user_id']))

        user_data = {'email': self.user.email, 'password': 'invalid_password'}
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        url = 'http://127.0.0.1:8000/auth/users/me/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        expected_data = {'username': 'foo', 'id': 1, 'email': 'foo@example.com'}
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_user_activity_endpoint(self):
        url = 'http://127.0.0.1:8000/api/account/user-activity/?user_id=1'
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)

        date_time_format = '%Y-%m-%d, %H:%M:%S'
        expected_data = {
            'status': 'success', 'user_id': 1,
            'last_login': f'{self.user.last_login.strftime(date_time_format)}',
            'last_request': f'{cache.get("1").strftime(date_time_format)}'
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = 'http://127.0.0.1:8000/api/account/user-activity/?user_id=2'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        expected_data = {'status': 'error', 'details': 'User with id <2> does not exist.'}
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, response.data)

        invalid_query_param = 'invalid'
        url = f'http://127.0.0.1:8000/api/account/user-activity/?{invalid_query_param}=1'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        expected_data = {'status': 'error', 'details': 'Query is incorrect, check your query parameters.'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, response.data)
