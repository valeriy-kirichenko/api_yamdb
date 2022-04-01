from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год',)
    category = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles'
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name="Жанр",
        related_name="titles",
        through='TitlesGenres'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitlesGenres(models.Model):
    work = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)


class Reviews(models.Model):
    work = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        related_name="review"
    )
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='review'
    )
    score = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="comments"
    )
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]
