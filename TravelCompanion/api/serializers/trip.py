from rest_framework import serializers

from .city import CitySerializer

from ..models.trip import Trip, TripCity
from ..models.user import User


class TripCitySerializer(serializers.ModelSerializer):
    """
    Used to serialize trip destinations.
    """
    class Meta:
        model = TripCity
        fields = ['city', 'flight_number']


class ReadonlyTripCitySerializer(TripCitySerializer):
    """
    Same as above, except that this serializer is meant for readonly operations.
    """
    city = CitySerializer()


class UserTripSerializer(serializers.ModelSerializer):
    """
    Serializer used to represent the initiator and participants of a trip.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ReadonlyTripSerializer(serializers.ModelSerializer):
    """
    The serializer used for readonly trip operations (list, retrieve --> GET).
    """
    initiator = UserTripSerializer(read_only=True)
    participants = UserTripSerializer(many=True, read_only=True)
    cities = ReadonlyTripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ['id', 'initiator', 'participants',
                  'cities', 'start_date', 'end_date', 'price']


class TripSerializer(serializers.ModelSerializer):
    """
    The serializer used for operations that mutate trips.
    Overrides update and create to add support for TripCity, the custom join model.
    """
    cities = TripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ReadonlyTripSerializer.Meta.fields

    def validate(self, attrs):
        """
        Performs additional check for the trip dates.
        """
        has_dates = 'start_date' in attrs and 'end_date' in attrs
        if has_dates and attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError(
                {'end_date': 'The end date must be after the start date.'})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        cities = validated_data.pop('tripcity_set', [])
        instance = super().update(instance, validated_data)

        for data in cities:
            TripCity.objects.update_or_create(**{'trip': instance, **data})

        instance.save()
        return instance

    def create(self, validated_data):
        # Nested objects insertion doesn't come out of the box, we need to handle this separately.
        cities = validated_data.pop('tripcity_set', [])
        trip = super().create(validated_data)

        for data in cities:
            TripCity.objects.create(**{'trip': trip, **data})

        return trip


class TripCitiesSerializer(serializers.ModelSerializer):
    """
    Serializer used to represent only the cities (destinations) attached to a trip.
    """
    cities = ReadonlyTripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ['cities']
