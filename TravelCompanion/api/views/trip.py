from rest_framework import viewsets

from ..models.trip import Trip
from ..serializers.trip import ReadonlyTripSerializer, TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        'initiator').prefetch_related('participants', 'cities')

    def get_serializer_class(self):
        is_read_action = self.action == 'list' or self.action == 'retrieve'
        return ReadonlyTripSerializer if is_read_action else TripSerializer
