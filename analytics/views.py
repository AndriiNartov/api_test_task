from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import LikeCountByDateFilter
from .serializers import LikeCountByDaySerializer
from post.models import Like


class GetLikesCountByDayAPIView(ListAPIView):
    '''
    Returns likes count by days range.
    Days range defines in query parameters
    "date_from" and "date_to" of GET request.
    Processing of date range implemented with custom filter.
    '''

    serializer_class = LikeCountByDaySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LikeCountByDateFilter

    def get_queryset(self):
        return Like.objects\
            .values('made_at')\
            .annotate(likes=Count('pk'))
