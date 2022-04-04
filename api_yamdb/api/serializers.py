from rest_framework import serializers, validators, generics
from rest_framework.permissions import SAFE_METHODS

from reviews.models import Title, Genre, Category, Review, Comments


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TitlesSerializer, self).__init__(*args, **kwargs)

        try:
            if self.context['request'].method in SAFE_METHODS:
                self.fields['category'] = CategoriesSerializer(read_only=True)
                self.fields['genre'] = GenresSerializer(
                    many=True, read_only=True
                )
        except KeyError:
            pass

    def get_rating(self, obj):
        if (
            self.context['request'].method in SAFE_METHODS
            and obj.rating is not None
        ):
            return int(obj.rating)
        return None


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return generics.get_object_or_404(
            Title,
            id=serializer_field.context['view'].kwargs.get('title_id')
        )


class CurrentReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return generics.get_object_or_404(
            Review,
            id=serializer_field.context['view'].kwargs.get('review_id')
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(min_value=1, max_value=10)
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message=('На произведение можно оставить '
                         'не более одного отзыва')
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.HiddenField(default=CurrentReviewDefault())

    class Meta:
        model = Comments
        fields = '__all__'
