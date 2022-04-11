from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import year_validator


class User(AbstractUser):
    """Пользователи"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),)
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text='Введите Username')
    email = models.EmailField('email', unique=True, max_length=254)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=max([len(role[0]) for role in ROLES]),
        choices=ROLES,
        default=USER)
    bio = models.TextField(verbose_name='О себе', null=True, blank=True, )
    confirmation_code = models.CharField(
        'Секретный код',
        max_length=4,
        blank=True, )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff


class CategoryGenreModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenreModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class TitlesGenres(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Title(models.Model):
    name = models.TextField(verbose_name='Название произведения')
    year = models.IntegerField(
        verbose_name='Год',
        validators=(year_validator,)
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitlesGenres'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class ReviewCommentModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]


class Review(ReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'


class Comments(ReviewCommentModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
