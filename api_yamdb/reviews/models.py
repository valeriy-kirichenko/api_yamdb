from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

ROLES = ('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')


class User(AbstractUser):
    """Модель для пользователя.

    Attributes:
        username (str): имя пользователя.
        email (str): электронная почта.
        first_name (str): имя.
        last_name (str): фамилия.
        role (str): роль.
        bio (str): о себе.
        confirmation_code (str): код подтверждения, для получения токена.
    """

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
        default='user')
    bio = models.TextField(verbose_name='О себе', null=True, blank=True, )
    confirmation_code = models.CharField(
        'Секретный код',
        max_length=4,
        blank=True, )

    @property
    def is_admin(self):
        """Проверяет является ли пользователь администратором.

        Returns:
            bool: True если пользователь администратор иначе False.
        """

        return self.role == User.ADMIN or self.is_staff


class CategoryGenreModel(models.Model):
    """Родительская модель для категории/жанра.

    Attributes:
        name (str): название.
        slug (str): уникальное название латиницей.
    """

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Возвращает строковое представление модели"""

        return self.name


class Category(CategoryGenreModel):
    """Модель для категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    """Модель для жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class TitlesGenres(models.Model):
    """Модель для связи произведений с жанрами.

    Attributes:
        title (int): id произведения.
        genre (int): id жанра.
    """

    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Title(models.Model):
    """Модель для произведения.

    Attributes:
        name (str): название произведения.
        year (int): год произведения.
        category (int): категория.
        description (str): описание.
        genre (int): жанр.
    """

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
        """Возвращает строковое представление модели"""

        return self.name


class ReviewCommentModel(models.Model):
    """Родительская модель для отзыва/комментария.

    Attributes:
        text (str): текст.
        author (int): id автора.
        pub_date (datetime): дата создания.
    """

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
        """Возвращает строковое представление модели"""

        return self.text[:30]


class Review(ReviewCommentModel):
    """Модель для отзыва.

    Attributes:
        title (int): id произведения.
        score (int): оценка.
    """

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
    """Модель для комментария.

    Attributes:
        review (int): id отзыва.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
