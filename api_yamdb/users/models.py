from django.contrib.auth.models import AbstractUser
from django.db import models


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
        help_text='Введите никнейм')

    email = models.EmailField('email', unique=True, max_length=254)

    first_name = models.CharField('Имя', max_length=150, blank=True)

    last_name = models.CharField('Фамилия', max_length=150, blank=True)

    role = models.CharField(
        verbose_name='Роль',
        max_length=max([len(role[0]) for role in ROLES]),
        choices=ROLES,
        default=USER)

    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True, )

    confirmation_code = models.CharField(
        'Секретный код',
        max_length=4,
        blank=True, )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff
