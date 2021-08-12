from django.db import models

from account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', related_name='posts')
    content = models.TextField(verbose_name='Content')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    def __str__(self):
        return f'id:{self.id}, author: {self.author}, created at: {self.creation_date.strftime("%Y-%m-%d, %H:%M")}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Author', related_name='likes', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='likes')
    made_at = models.DateField(auto_now_add=True, verbose_name='Like date')
