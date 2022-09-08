from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse


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

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    # We have to redefine save() function to auto-generate
    # a slug for a new instance
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title
