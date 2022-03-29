from django.contrib.auth import get_user_model
from django.db import models

# from users import User

User = get_user_model()


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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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
    works = models.ManyToManyField(
        Titles, verbose_name="Произведения", related_name="works"
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    work = models.OneToOneField(
        Titles,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        related_name="work"
    )
    text = models.TextField(verbose_name="Отзыв")

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    review = models.OneToOneField(
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
