import re

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from rest_framework import serializers, generics
from rest_framework.permissions import SAFE_METHODS
from reviews.models import Title, Genre, Category, Review, Comments, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: "{username}"')
        if re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: "{username}"')
        return username


class EditProfileSerializer(UserSerializer):
    """Сериализатор редактирования профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(required=True, max_length=150, )
    email = serializers.EmailField(required=True, max_length=254, )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                f'Запрещено называть Username: {username}')
        return username

    def validate(self, data):
        name_search_in_db = User.objects.filter(username=data.get('username'))
        email_search_in_db = User.objects.filter(email=data.get('email'))
        if name_search_in_db or email_search_in_db:
            raise serializers.ValidationError('Дублирование в базе данных!')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    username = serializers.CharField(required=True, max_length=150, )
    confirmation_code = serializers.CharField(required=True, )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ReadTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


class WriteTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = generics.get_object_or_404(
                Title,
                id=self.context['request'].parser_context['kwargs'].get(
                    'title_id')
            )
            if Review.objects.filter(
                title_id=title.id,
                author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    detail=('На произведение можно оставить '
                            'не более одного отзыва'),
                    code=400
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = generics.get_object_or_404(
                Title,
                id=self.context['request'].parser_context['kwargs'].get(
                    'title_id')
            )
            if not Review.objects.filter(
                title_id=title.id,
                author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    detail=('Отзыв не найден'),
                    code=400
                )
        return data

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
