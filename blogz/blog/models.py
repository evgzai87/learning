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
    RUSSIA = '1'
    WORLD = '2'
    EX_USSR = '3'
    ECONOMY = '4'
    FORCE_STRUCTURES = '5'
    SCIENCE_AND_TECHNOLOGY = '6'
    CULTURE = '7'
    SPORT = '8'
    INTERNET_AND_MASS_MEDIA = '9'
    VALUES = '10'
    TRAVELS = '11'
    FROM_THE_LIFE = '12'

    CATEGORY = (
        (None, 'Выберите категорию'),
        (RUSSIA, 'Россия'),
        (WORLD, 'Мир'),
        (EX_USSR, 'Бывший СССР'),
        (ECONOMY, 'Экономика'),
        (FORCE_STRUCTURES, 'Силовые структуры'),
        (SCIENCE_AND_TECHNOLOGY, 'Наука и техника'),
        (CULTURE, 'Культура'),
        (SPORT, 'Спорт'),
        (INTERNET_AND_MASS_MEDIA, 'Интернет и СМИ'),
        (VALUES, 'Ценности'),
        (TRAVELS, 'Путешествия'),
        (FROM_THE_LIFE, 'Из жизни')
    )

    title = models.CharField(verbose_name='Название статьи', max_length=100)
    content = models.TextField(verbose_name='Содержание статьи')
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='%Y/%m/%d/',
        blank=True
    )
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(
        max_length=2,
        choices=CATEGORY
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title
