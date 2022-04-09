from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, registration, get_token

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)

auth_urls = [
    path('auth/signup/', registration, name='registration'),
    path('auth/token/', get_token, name='get_token')
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(auth_urls))
]
