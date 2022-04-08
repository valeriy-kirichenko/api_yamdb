import re

from rest_framework import serializers, generics

from reviews.models import Title, Genre, Category, Review, Comments, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя "{username}"')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с никнеймом "{username}" уже зарегистрирован')
        elif re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя "{username}"')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Email: {email} уже зарегистрирован')
        return email


class EditProfileSerializer(UserSerializer):
    """Сериализатор редактирования профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegistrationSerializer(UserSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta(UserSerializer.Meta):
        fields = ('username', 'email')


class TokenSerializer(UserSerializer):
    """Сериализатор токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta(UserSerializer.Meta):
        fields = ('username', 'confirmation_code')


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
        read_only_fields = ('category', 'genre', 'rating')


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
    title = serializers.HiddenField(
        default=serializers.SerializerMethodField('get_title')
    )

    def get_title(self):
        return generics.get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def validate(self, data):
        title = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        review = Review.objects.filter(title_id=title, author=author)
        if self.context['request'].method == 'POST':
            if review.exists():
                raise serializers.ValidationError(
                    detail=('На произведение можно оставить '
                            'не более одного отзыва'),
                    code=400
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    review = serializers.HiddenField(
        default=serializers.SerializerMethodField('get_review')
    )

    def get_review(self):
        return generics.get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date', 'review')
