from django.test import TestCase

from post.serializers import PostCreateSerializer


class PostSerializersTestCase(TestCase):

    def test_post_create_serializer(self):
        post_creation_data = {
            'content': 'Hi, it is the test post here!',
        }
        data = PostCreateSerializer(post_creation_data).data
        expected_data = {
            'content': 'Hi, it is the test post here!',
        }
        self.assertEqual(expected_data, data)

        some_invalid_field_name = 'invalid'
        some_invalid_data = {
            f'{some_invalid_field_name}': 'Hi, it is the test post here!',
        }
        with self.assertRaises(KeyError):
            print(PostCreateSerializer(some_invalid_data).data)
