# Generated by Django 4.1 on 2022-09-05 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d', verbose_name='Картинки'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[(None, 'Выберите категорию'), ('1', 'Россия'), ('2', 'Мир'), ('3', 'Бывший СССР'), ('4', 'Экономика'), ('5', 'Силовые структуры'), ('6', 'Наука и техника'), ('7', 'Культура'), ('8', 'Спорт'), ('9', 'Интернет и СМИ'), ('10', 'Ценности'), ('11', 'Путешествия'), ('12', 'Из жизни')], max_length=2),
        ),
    ]