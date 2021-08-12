from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, verbose_name='Email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
