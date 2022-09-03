from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(models.Model):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=20,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        blank=True
    )  # not required
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20,
        blank=True
    )  # not required
    email = models.EmailField(
        verbose_name='Email адрес',
        unique=True
    )
    registration_date = models.DateTimeField(
        verbose_name='Дата регистрации',
        default=timezone.now
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('1', 'Россия'),
        ('2', 'Мир'),
        ('3', 'Бывший СССР'),
        ('4', 'Экономика'),
        ('5', 'Силовые структуры'),
        ('6', 'Наука и техника'),
        ('7', 'Культура'),
        ('8', 'Спорт'),
        ('9', 'Интернет и СМИ'),
        ('10', 'Ценности'),
        ('11', 'Путешествия'),
        ('12', 'Из жизни')
    )

    title = models.CharField(verbose_name='Название статьи', max_length=100)
    content = models.TextField(verbose_name='Содержание статьи')
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='1'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title
