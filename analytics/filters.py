from django_filters import rest_framework as filters

from post.models import Like


class LikeCountByDateFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='made_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='made_at', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ['made_at']
