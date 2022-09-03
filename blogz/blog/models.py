from django.db import models
from django.utils import timezone
from django.utils.text import slugify


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

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Article(models.Model):
    CATEGORIES = [
        'Россия',
        'Мир',
        'Бывший СССР',
        'Экономика',
        'Силовые структуры',
        'Наука и техника',
        'Культура',
        'Спорт',
        'Интернет и СМИ',
        'Ценности',
        'Путешествия',
        'Из жизни',
        'Среда обитания',
        'Забота о себе'
    ]

    title = models.CharField(verbose_name='Название статьи', max_length=100)
    content = models.TextField(verbose_name='Содержание статьи')
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title
