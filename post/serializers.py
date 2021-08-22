from rest_framework import serializers

from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # fields = ('id', 'content')
        fields = '__all__'
