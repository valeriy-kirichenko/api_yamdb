from rest_framework import serializers, validators
from rest_framework.permissions import SAFE_METHODS

from reviews.models import Titles, Genres, Categories, Reviews, Comments


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        many=True,
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
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


class CurrentWorkDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return Titles.objects.get(
            id=serializer_field.context['view'].kwargs.get('title_id')
        )


class CurrentReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return Reviews.objects.get(
            id=serializer_field.context['view'].kwargs.get('review_id')
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(min_value=1, max_value=10)
    work = serializers.HiddenField(default=CurrentWorkDefault())

    class Meta:
        model = Reviews
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('work', 'author'),
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
