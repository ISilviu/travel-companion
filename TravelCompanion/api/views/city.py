from rest_framework import viewsets

from ..models.city import City
from ..serializers.city import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer