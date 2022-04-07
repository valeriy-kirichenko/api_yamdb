from django.db.utils import IntegrityError
from rest_framework import serializers, validators, generics
from rest_framework.permissions import SAFE_METHODS

from reviews.models import Title, Genre, Category, Review, Comments


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
