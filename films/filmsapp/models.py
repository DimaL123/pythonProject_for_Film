from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Категорія", max_length=150)
    description = models.TextField("Опис")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Actor(models.Model):
    name = models.CharField("Ім'я", max_length=60)
    age = models.PositiveSmallIntegerField("Вік", default=0)
    description = models.TextField("Опис")
    image = models.ImageField("Зображення", upload_to="actotrs/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актори та режисери"
        verbose_name_plural = "Актори та режисери"


class Genre(models.Model):  # жанр
    name = models.CharField("Жанр", max_length=150)
    description = models.TextField("Опис")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Film(models.Model):
    title = models.CharField("Назва", max_length=150)
    tagline = models.CharField("Гасло", max_length=150, default='')
    description = models.TextField("Опис")
    poster = models.ImageField("Зображення фільму", upload_to="poster_img/")
    uear = models.PositiveSmallIntegerField("Рік виходу", default=2019)
    country = models.CharField("Країна", max_length=30)

    actors = models.ManyToManyField(Actor, verbose_name="Актори", related_name="film_actor")
    director = models.ManyToManyField(Actor, verbose_name="Режисер", related_name="film_director")
    genre = models.ManyToManyField(Genre, verbose_name="Жанри")

    world_premiere = models.DateField("Примєра", default=date.today)
    budget = models.PositiveSmallIntegerField("Бюджет", default=0)

    fees_usa = models.PositiveSmallIntegerField("USA", default=0, help_text="Вказати суму в $")
    fees_world = models.PositiveSmallIntegerField("World", default=0, help_text="Вказати суму в $")

    category = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Чернетка", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("film_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"


class FilmImages(models.Model):
    title = models.CharField("Назва", max_length=150)
    description = models.TextField("Опис")
    image = models.ImageField("Зображення фільму", upload_to="film_img/")
    film = models.ForeignKey(Film, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр з фільму"
        verbose_name_plural = "Кадри з фільму"


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значення", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Зірка рейтингу"
        verbose_name_plural = "Зірки рейтингу"
        ordering = ["-value"]


class Rating(models.Model):
    pi = models.CharField("IP адреса", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Зірка", on_delete=models.CASCADE)
    film = models.ForeignKey(Film, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star}-{self.film}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=30)
    text = models.TextField("Коментар", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Батько", on_delete=models.SET_NULL, blank=True, null=True)
    film = models.ForeignKey(Film, verbose_name="фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.film}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
