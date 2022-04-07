from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, registration, get_token

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='users')

v1_auth_urls = [
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token')
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('', include(v1_auth_urls))
]
