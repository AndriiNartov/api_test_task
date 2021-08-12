from rest_framework import status
from rest_framework.test import APITestCase

from datetime import datetime, timedelta

from account.models import User
from analytics.serializers import LikeCountByDaySerializer
from analytics.views import GetLikesCountByDayAPIView
from post.models import Like, Post


class LikesCountByDayAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='foo@example.com', username='foo', password='Aa123456!')
        self.post = Post.objects.create(author=self.user, content='I am the setUp POST!!!')
        self.post_1 = Post.objects.create(author=self.user, content='I am the setUp POST_1!!!')
        self.post_2 = Post.objects.create(author=self.user, content='I am the setUp POST_2!!!')
        self.post_3 = Post.objects.create(author=self.user, content='I am the setUp POST_3!!!')
        self.post_4 = Post.objects.create(author=self.user, content='I am the setUp POST_4!!!')
        self.like = Like.objects.create(author=self.user, post=self.post)
        self.like_1 = Like.objects.create(author=self.user, post=self.post_1)
        self.like_2 = Like.objects.create(author=self.user, post=self.post_2)
        self.like_3 = Like.objects.create(author=self.user, post=self.post_3)
        self.like_4 = Like.objects.create(author=self.user, post=self.post_4)
        jwt_creation_url = 'http://127.0.0.1:8000/auth/jwt/create'
        user_data = {'email': self.user.email, 'password': 'Aa123456!'}
        response = self.client.post(jwt_creation_url, user_data, format='json')
        self.token = response.data['access']

    def test_likes_count_by_day(self):
        one_day_delta = timedelta(days=1)
        two_days_delta = timedelta(days=2)
        today = datetime.now().date()
        yesterday = today - one_day_delta
        day_before_yesterday = today - two_days_delta

        self.like.made_at = day_before_yesterday
        self.like_1.made_at = day_before_yesterday
        self.like_2.made_at = yesterday
        self.like.save()
        self.like_1.save()
        self.like_2.save()

        view_object = GetLikesCountByDayAPIView()
        queryset = view_object.get_queryset()

        url = f'http://127.0.0.1:8000/api/analytics/likes-by-day/?date_from={day_before_yesterday}&date_to={today}'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)

        expected_data = LikeCountByDaySerializer(queryset, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = f'http://127.0.0.1:8000/api/analytics/likes-by-day/?date_from={day_before_yesterday}&date_to=2021-13-13'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
