# Generated by Django 4.1 on 2022-08-31 13:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='Имя пользователя')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Email адрес')),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название статьи')),
                ('content', models.TextField(verbose_name='Содержание статьи')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user', verbose_name='Автор')),
            ],
        ),
    ]
