from rest_framework import serializers
from ..models.trip import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['initiator', 'participants', 'cities', 'start_date', 'end_date', 'price']
