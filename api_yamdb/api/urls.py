from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitlesViewSet, CategoriesViewSet, GenresViewSet,
                    ReviewsViewSet, CommentsViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
