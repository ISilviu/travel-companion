from ..models.user import User
from rest_framework import serializers

from .trip import ReadonlyTripSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    The serializer used for all the available operations at the /users endpoint.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'groups', 'is_superuser']

    def create(self, validated_data):
        """
        Explicitly call set_password to ensure the password is hashed.
        """
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class ReadonlyInitiatedTripsSerializer(serializers.ModelSerializer):
    """
    Used to serialize a certain user's trips.
    """
    initiated_trips = ReadonlyTripSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['initiated_trips']
