from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, generics, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAuthorOrStaffOrReadOnly, IsAdminOrReadOnly)
from .serializers import (ReadTitleSerializer, CommentsSerializer,
                          GenreSerializer, CategorySerializer,
                          ReviewsSerializer, WriteTitleSerializer)
from core.models import CategoriesGenresViewSet
from reviews.models import Title, Genre, Category, Review


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = TitleFilter
    search_fields = ('name',)
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadTitleSerializer
        return WriteTitleSerializer


class CategoriesViewSet(CategoriesGenresViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CategoriesGenresViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


def get_title(title_id):
    return generics.get_object_or_404(Title, id=title_id)


def get_review(review_id, title_id):
    return generics.get_object_or_404(
        Review,
        id=review_id,
        title=get_title(title_id)
    )


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return get_title(self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_title(self.kwargs.get('title_id'))
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('text',)

    def get_queryset(self):
        return get_review(
            self.kwargs.get('review_id'), self.kwargs.get('title_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_review(
                self.kwargs.get('review_id'), self.kwargs.get('title_id')
            )
        )
