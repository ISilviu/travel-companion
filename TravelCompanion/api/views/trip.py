from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from ..models.trip import Trip
from ..serializers.trip import ReadonlyTripSerializer, TripCitiesSerializer, TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        'initiator').prefetch_related('participants', 'cities')

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        is_read_action = self.action == 'list' or self.action == 'retrieve'
        return ReadonlyTripSerializer if is_read_action else TripSerializer

    @action(detail=True)
    def cities(self, request, pk):
        trip = Trip.objects.filter(id=pk).first()
        if trip is None:
            return Response('Trip not found.', status=status.HTTP_404_NOT_FOUND)

        trips = TripCitiesSerializer(trip).data
        return Response(trips, status=status.HTTP_200_OK)
