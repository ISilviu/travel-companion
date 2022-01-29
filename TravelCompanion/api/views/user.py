from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.user import InitiatedTripsSerializer, ReadonlyInitiatedTripsSerializer, UserSerializer, GroupSerializer
from ..models.user import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related(
        'participating_trips', 'initiated_trips')
    serializer_class = UserSerializer

    @action(detail=True, methods=['get', 'post, put'])
    def trips(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

        methods_serializers = {
            'GET': ReadonlyInitiatedTripsSerializer,
            'POST': InitiatedTripsSerializer
        }
        serializer_class = methods_serializers[request.method]
        trips = serializer_class(user).data
        return Response(trips, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
