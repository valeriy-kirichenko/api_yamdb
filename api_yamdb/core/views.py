from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly


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
