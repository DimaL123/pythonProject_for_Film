# Generated by Django 5.0.2 on 2024-02-14 14:18

import datetime
import django.db.models.deletion
import django.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name="Ім'я")),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name='Вік')),
                ('description', models.TextField(verbose_name='Опис')),
                ('image', models.ImageField(upload_to='actotrs/', verbose_name='Зображення')),
            ],
            options={
                'verbose_name': 'Актори та режисери',
                'verbose_name_plural': 'Актори та режисери',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категорія')),
                ('description', models.TextField(verbose_name='Опис')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Жанр')),
                ('description', models.TextField(verbose_name='Опис')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанри',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значення')),
            ],
            options={
                'verbose_name': 'Зірка рейтингу',
                'verbose_name_plural': 'Зірки рейтингу',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Назва')),
                ('tagline', models.CharField(default='', max_length=150, verbose_name='Гасло')),
                ('description', models.TextField(verbose_name='Опис')),
                ('poster', models.ImageField(upload_to='poster_img/', verbose_name='Зображення фільму')),
                ('uear', models.PositiveSmallIntegerField(default=2019, verbose_name='Рік виходу')),
                ('country', models.CharField(max_length=30, verbose_name='Країна')),
                ('world_premiere', models.DateField(default=datetime.date.today, verbose_name='Примєра')),
                ('budget', models.PositiveSmallIntegerField(default=0, verbose_name='Бюджет')),
                ('fees_usa', models.PositiveSmallIntegerField(default=0, help_text='Вказати суму в $', verbose_name='USA')),
                ('fees_world', models.PositiveSmallIntegerField(default=0, help_text='Вказати суму в $', verbose_name='World')),
                ('url', models.SlugField(max_length=160, unique=True)),
                ('draft', models.BooleanField(default=False, verbose_name='Чернетка')),
                ('actors', models.ManyToManyField(related_name='film_actor', to='filmsapp.actor', verbose_name='Актори')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='filmsapp.category', verbose_name='Категорія')),
                ('director', models.ManyToManyField(related_name='film_director', to='filmsapp.actor', verbose_name='Режисер')),
                ('genre', models.ManyToManyField(to='filmsapp.genre', verbose_name='Жанри')),
            ],
            options={
                'verbose_name': 'Фільм',
                'verbose_name_plural': 'Фільми',
            },
        ),
        migrations.CreateModel(
            name='FilmImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Назва')),
                ('description', models.TextField(verbose_name='Опис')),
                ('image', models.ImageField(upload_to='film_img/', verbose_name='Зображення фільму')),
                ('films', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmsapp.films', verbose_name='Фільм')),
            ],
            options={
                'verbose_name': 'Кадр з фільму',
                'verbose_name_plural': 'Кадри з фільму',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pi', models.CharField(max_length=15, verbose_name='IP адреса')),
                ('films', models.ForeignKey(on_delete=django.db.models.fields.CharField, to='filmsapp.films', verbose_name='Фільм')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmsapp.ratingstar', verbose_name='Зірка')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=30, verbose_name="Ім'я")),
                ('text', models.TextField(max_length=5000, verbose_name='Коментар')),
                ('films', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmsapp.films', verbose_name='фільм')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filmsapp.reviews', verbose_name='Батько')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
            },
        ),
    ]