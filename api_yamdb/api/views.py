from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import IsAdmin, IsAuthorOrStaffOrReadOnly, IsAdminOrReadOnly
from .serializers import (ReadTitleSerializer, CommentsSerializer,
                          GenreSerializer, CategorySerializer,
                          ReviewsSerializer, WriteTitleSerializer,
                          UserSerializer, EditProfileSerializer,
                          RegistrationSerializer, TokenSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from core.views import CategoriesGenresViewSet
from reviews.models import Title, Genre, Category, Review, User

OK = 200
BAD_REQUEST = 400
METHOD_NOT_ALLOWED = 405


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginathion_class = (LimitOffsetPagination,)
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=EditProfileSerializer)
    def get_and_edit_self_profile(self, request):
        """Получение и редактирование профиля."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True, )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=OK)
        return Response(status=METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """Регистрация."""
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if not User.objects.filter(
            username=serializer.validated_data['username']
        ).exists():
            serializer.save()
        user = generics.get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Registration',
            message=f'Your code: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=OK)
    return Response(serializer.errors, status=BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = generics.get_object_or_404(
        User,
        username=serializer.validated_data['username'], )
    if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({'token': token}, status=OK)
    return Response(serializer.errors, status=BAD_REQUEST)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
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
