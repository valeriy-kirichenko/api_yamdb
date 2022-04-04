from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, registration, get_token

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', registration, name='registration'),
    path('auth/token/', get_token, name='get_token')
]
