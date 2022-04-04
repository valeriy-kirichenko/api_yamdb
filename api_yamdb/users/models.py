from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователи"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    DEFAULT_USER = 'user'
    ROLES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (DEFAULT_USER, 'User'),)

    role = models.CharField(
        verbose_name='Роль',
        max_length=79,
        choices=ROLES,
        default=DEFAULT_USER)

    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )
