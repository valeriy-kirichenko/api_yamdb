from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitlesViewSet, CategoriesViewSet, GenresViewSet,
                    ReviewsViewSet, CommentsViewSet, UserViewSet,
                    registration, get_token)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
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

auth_urls = [
    path('signup/', registration, name='registration'),
    path('token/', get_token, name='get_token')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
