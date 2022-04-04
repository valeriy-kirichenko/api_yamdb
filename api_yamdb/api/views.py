from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics, filters, permissions
from rest_framework.pagination import LimitOffsetPagination

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrStaffOrReadOnly, SAFE_METHODS)
from .serializers import (TitlesSerializer, CommentsSerializer,
                          GenresSerializer, CategoriesSerializer,
                          ReviewsSerializer)
from reviews.models import Title, Genre, Category, Review


class MixinSet(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitlesSerializer
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = TitleFilter
    search_fields = ('name',)
    ordering_fields = ('name',)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (IsAdmin(),)


class CategoriesViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        title = generics.get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.review.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = generics.get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('text',)

    def get_queryset(self):
        review = generics.get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
