from rest_framework import serializers

from post.models import Like


class LikeCountByDaySerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='made_at')
    likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('date', 'likes')
