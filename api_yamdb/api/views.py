from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import (IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly,
                          SAFE_METHODS)
from .serializers import (TitlesSerializer, CommentsSerializer,
                          GenresSerializer, CategoriesSerializer,
                          ReviewsSerializer)
from reviews.models import Titles, Genres, Categories, Reviews


class MixinSet(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitlesSerializer
    permission_class = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('category', 'genre')
    search_fields = ('name',)
    ordering_fields = ('name',)


class CategoriesViewSet(MixinSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    lookup_field = 'slug'


class GenresViewSet(MixinSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return (IsAuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        work = generics.get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        return work.review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('text',)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return (IsAuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        review = generics.get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
