from rest_framework.test import APITestCase
from rest_framework import status

from account.models import User
from post.models import Post


class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='foo@example.com', username='foo', password='Aa123456!')
        self.post = Post.objects.create(author=self.user, content='I am the setUp POST!!!')
        jwt_creation_url = 'http://127.0.0.1:8000/auth/jwt/create'
        user_data = {'email': self.user.email, 'password': 'Aa123456!'}
        response = self.client.post(jwt_creation_url, user_data, format='json')
        self.token = response.data['access']

    def test_post_create(self):
        url = 'http://127.0.0.1:8000/api/post/create/'
        post_content = {'content': 'This is a new post!'}
        response = self.client.post(url, post_content)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, post_content)
        expected_data = {'id': 2, 'content': 'This is a new post!'}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

        post_content = {}
        response = self.client.post(url, post_content)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_like_unlike(self):
        url = 'http://127.0.0.1:8000/api/post/1/like/'
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url)
        expected_data = {'post_id': '1', 'status': True, 'details': 'Post was successfully liked.'}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

        response = self.client.post(url)
        expected_data = {'post_id': '1', 'status': False, 'details': 'Post was successfully unliked.'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = 'http://127.0.0.1:8000/api/post/2/like/'
        response = self.client.post(url)
        expected_data = {'post_id': '2', 'status': 'error', 'details': 'Post with id <2> does not exist.'}
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, response.data)
