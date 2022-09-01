from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=20,
        unique=True
    )
    first_name = models.CharField(verbose_name='Имя', max_length=20)  # not required
    last_name = models.CharField(verbose_name='Фамилия', max_length=20)  # not required
    email = models.EmailField(verbose_name='Email адрес', unique=True)
    registration_date = models.DateTimeField(
        verbose_name='Дата регистрации',
        default=timezone.now)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='Название статьи', max_length=100)
    content = models.TextField(verbose_name='Содержание статьи')
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
