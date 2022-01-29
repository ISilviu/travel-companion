from django.contrib.auth.models import Group
from ..models.user import User
from rest_framework import serializers

from .trip import ReadonlyTripSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'groups', 'participating_trips', 'initiated_trips']


class InitiatedTripsSerializer(serializers.ModelSerializer):
    trips = ReadonlyTripSerializer(
        source='initiated_trips', read_only=True, many=True)

    class Meta:
        model = User
        fields = ['trips']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
