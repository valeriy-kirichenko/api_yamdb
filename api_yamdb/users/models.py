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
        max_length=max([len(role[0]) for role in ROLES]),
        choices=ROLES,
        default=DEFAULT_USER)

    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True, )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff or self.is_superuser

    def __str__(self):
        return self.username
