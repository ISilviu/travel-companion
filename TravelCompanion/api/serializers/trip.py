from rest_framework import serializers

from .city import CitySerializer

from ..models.trip import Trip, TripCity
from ..models.user import User


class TripCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCity
        fields = ['trip', 'city', 'flight_number']


class UserTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TripCitySerializer(serializers.ModelSerializer):
    city = CitySerializer()
    class Meta:
        model = TripCity
        fields = ['city', 'flight_number']


class ReadonlyTripSerializer(serializers.ModelSerializer):
    initiator = UserTripSerializer(read_only=True)
    participants = UserTripSerializer(many=True, read_only=True)
    cities = TripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ['id', 'initiator', 'participants',
                  'cities', 'start_date', 'end_date', 'price']


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ReadonlyTripSerializer.Meta.fields


class TripCitiesSerializer(serializers.ModelSerializer):
    cities = TripCitySerializer(source='tripcity_set', many=True)
    class Meta:
        model = Trip
        fields = ['cities']
