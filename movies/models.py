from datetime import date

from django.db import models


class Category(models.Model):
    """Категорії"""
    name = models.CharField('Категорія', max_length=150)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Actor(models.Model):
    """Актори та режисери"""
    name = models.CharField("Ім'я", max_length=100)
    age = models.PositiveSmallIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField("Зображення", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актори та режисери'
        verbose_name_plural = 'Актори та режисери'


class Genge(models.Model):
    """Жанри"""
    name = models.CharField("Назва жанру", max_length=150)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    """Фільми"""
    title = models.CharField("Назва", max_length=100)
    tagline = models.CharField("Гасло", max_length=100, default='')
    description = models.TextField('Опис')
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата екранізації", default=2019)
    country = models.CharField("Країна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режисер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актори", related_name="film_actor")
    genres = models.ManyToManyField(Genge, verbose_name="жанри")
    world_premiere = models.DateField("Прем'єра в світі", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="вказать суму в доларах США")
    fees_in_usa = models.PositiveIntegerField("Касові сбори в США", default=0,
                                              help_text="вказать суму в доларах США")
    fees_in_world = models.PositiveIntegerField("Касові сбори у світі", default=0,
                                                help_text="вказать суму в доларах США")
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Чорновик", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class MovieShots(models.Model):
    """Кадри з фільму"""
    title = models.CharField("Назва", max_length=100)
    description = models.TextField('Опис')
    image = models.ImageField("Зображення", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр з фільму'
        verbose_name_plural = 'Кадри з фільму'


class RatingStar(models.Model):
    """Зірочка рейтингу"""
    value = models.SmallIntegerField("Занчення", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Зірочка рейтингу'
        verbose_name_plural = 'Зірочки рейтингу'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("ІР адреса", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="зірочка")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фільм")

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviwes(models.Model):
    """Відгуки"""
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=100)
    text = models.TextField("Повідомлення", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="предок",
                               on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

