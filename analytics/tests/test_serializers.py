from django.test import TestCase

from collections import OrderedDict

from account.models import User
from analytics.serializers import LikeCountByDaySerializer
from analytics.views import GetLikesCountByDayAPIView
from post.models import Like, Post


class AnalyticsSerializersTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='foo@example.com', username='foo', password='Aa123456!')
        self.post = Post.objects.create(author=self.user, content='I am the setUp POST!!!')
        self.like = Like.objects.create(author=self.user, post=self.post)

    def test_likes_count_by_day(self):
        view_object = GetLikesCountByDayAPIView()
        queryset = view_object.get_queryset()
        data = LikeCountByDaySerializer(queryset, many=True).data
        expected_data = [OrderedDict([('date', f'{self.like.made_at}'), ('likes', 1)])]
        self.assertEqual(expected_data, data)
