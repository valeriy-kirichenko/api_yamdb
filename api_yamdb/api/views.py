from rest_framework import viewsets

from .serializers import TitlesSerializer
from reviews.models import Titles


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
