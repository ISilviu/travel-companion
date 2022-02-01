from django.contrib.auth.models import Group
from ..models.user import User
from rest_framework import serializers

from .trip import ReadonlyTripSerializer, TripSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    The serializer used for all the available operations at the /users endpoint.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'groups', 'participating_trips', 'initiated_trips']


class ReadonlyInitiatedTripsSerializer(serializers.ModelSerializer):
    """
    Used to serialize a certain user's trips.
    """
    initiated_trips = ReadonlyTripSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['initiated_trips']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
