from django.contrib.auth import get_user_model
from django.db import models

# from users import User

User = get_user_model()


class Categories(models.Model):
    title = models.CharField(
        max_length=35,
        verbose_name='Категория'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Titles(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название произведения'
    )
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
        return self.title
