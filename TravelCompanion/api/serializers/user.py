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
    class Meta:
        model = User
        fields = ['initiated_trips']


class ReadonlyInitiatedTripsSerializer(InitiatedTripsSerializer):
    initiated_trips = ReadonlyTripSerializer(read_only=True, many=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
