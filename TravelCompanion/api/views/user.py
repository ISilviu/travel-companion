from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from ..serializers.user import ReadonlyInitiatedTripsSerializer, UserSerializer
from ..models.user import User

class CreateOnlyPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return True if view.action == 'create' else super().has_permission(request, view)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related(
        'participating_trips', 'initiated_trips')
    serializer_class = UserSerializer
    permission_classes = [CreateOnlyPermission]

    @action(detail=True)
    def trips(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

        trips = ReadonlyInitiatedTripsSerializer(user).data
        return Response(trips, status=status.HTTP_200_OK)
