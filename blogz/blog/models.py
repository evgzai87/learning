from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(verbose_name='Название статьи', max_length=100)
    content = models.TextField(verbose_name='Содержание статьи')
    publication_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.username
