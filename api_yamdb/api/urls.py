from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitlesViewSet

router_v1 = DefaultRouter()

router_v1.register(r'titles', TitlesViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
