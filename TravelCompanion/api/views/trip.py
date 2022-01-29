from rest_framework import viewsets

from ..models.trip import Trip
from ..serializers.trip import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related('initiator').prefetch_related('participants', 'cities')
    serializer_class = TripSerializer