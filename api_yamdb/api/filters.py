from django_filters import FilterSet, rest_framework

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтрует выдачу произведений."""

    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
