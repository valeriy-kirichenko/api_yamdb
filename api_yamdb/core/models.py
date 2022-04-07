from django.db import models
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly


class CategoryGenreModel(models.Model):
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReviewCommentModel(models.Model):
    text = models.TextField()
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


class CreateListDestroyModelMixinSet(mixins.CreateModelMixin,
                                     mixins.ListModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    pass


class CategoriesGenresViewSet(CreateListDestroyModelMixinSet):
    permission_classes = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    class Meta:
        abstract = True
