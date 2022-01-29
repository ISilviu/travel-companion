from rest_framework import serializers
from ..models.trip import Trip, TripCity


class TripCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCity
        fields = ['trip', 'city', 'flight_number']


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['initiator', 'participants',
                  'cities', 'start_date', 'end_date', 'price']
