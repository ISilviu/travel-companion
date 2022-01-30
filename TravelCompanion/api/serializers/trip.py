from rest_framework import serializers

from .city import CitySerializer

from ..models.trip import Trip, TripCity
from ..models.user import User


class ReadonlyTripCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCity
        fields = ['trip', 'city', 'flight_number']


class UserTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TripCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCity
        fields = ['city', 'flight_number']


class ReadonlyTripCitySerializer(TripCitySerializer):
    city = CitySerializer()


class ReadonlyTripSerializer(serializers.ModelSerializer):
    initiator = UserTripSerializer(read_only=True)
    participants = UserTripSerializer(many=True, read_only=True)
    cities = ReadonlyTripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ['id', 'initiator', 'participants',
                  'cities', 'start_date', 'end_date', 'price']


class TripSerializer(serializers.ModelSerializer):
    cities = TripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ReadonlyTripSerializer.Meta.fields

    def validate(self, attrs):
        has_dates = 'start_date' in attrs and 'end_date' in attrs
        if has_dates and attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError(
                {'end_date': 'The end date must be after the start date.'})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        cities = validated_data.pop('tripcity_set')
        instance = super().update(instance, validated_data)

        for data in cities:
            TripCity.objects.update_or_create(**{'trip': instance, **data})

        instance.save()
        return instance

    def create(self, validated_data):
        # Nested objects insertion doesn't come out of the box, we need to handle this separately.
        cities = validated_data.pop('tripcity_set')
        trip = super().create(validated_data)

        for data in cities:
            TripCity.objects.create(**{'trip': trip, **data})

        return trip


class TripCitiesSerializer(serializers.ModelSerializer):
    cities = ReadonlyTripCitySerializer(source='tripcity_set', many=True)

    class Meta:
        model = Trip
        fields = ['cities']
