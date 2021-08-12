from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .models import Like, Post
from .serializers import PostCreateSerializer


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeUnlikeAPIView(GenericAPIView):
    '''
    This API View is the same for "like" and "unlike" actions.
    I use this solution, because in social networks
    (on the frontend) "like" and "unlike" are almost always
    the same button.
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        author = request.user
        try:
            post = Post.objects.get(id=kwargs['pk'])
            like, created = Like.objects.get_or_create(
                author=author,
                post=post
            )
            if created:
                return Response(
                    {
                        'post_id': f'{post.id}',
                        'status': True,
                        'details': 'Post was successfully liked.'
                    },
                    status=HTTP_201_CREATED
                )
            else:
                like.delete()
                return Response(
                    {
                        'post_id': f'{post.id}',
                        'status': False,
                        'details': 'Post was successfully unliked.'
                    },
                    status=HTTP_200_OK
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'post_id': f'{kwargs["pk"]}',
                    'status': 'error',
                    'details': f'Post with id <{kwargs["pk"]}> does not exist.'
                },
                status=HTTP_404_NOT_FOUND
            )
