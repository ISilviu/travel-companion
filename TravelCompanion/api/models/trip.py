from django.db import models
from .user import User
from .city import City


class Trip(models.Model):
    """
    The trip model, consisting of the following fields:
    - initiator - the user that initiated the trip
    - participants - the other users that joined the trip
    - cities - the cities (destinations) of the trip
    - start_date, end_date - the begin and end dates of the trip
    - price - the total price of the trip
    """
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='initiated_trips')
    participants = models.ManyToManyField(
        User, related_name='participating_trips', blank=True)
    cities = models.ManyToManyField(City, through='TripCity')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    price = models.PositiveBigIntegerField(null=True)


class TripCity(models.Model):
    """
    The join entity between Trip and City. 
    Contains the flight number as an extra field, could be extended to include further details like reservations.
    """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=50)
