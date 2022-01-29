from django.db import models
from .user import User
from .city import City


class Trip(models.Model):
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='initiated_trips')
    participants = models.ManyToManyField(
        User, related_name='participating_trips', blank=True)
    cities = models.ManyToManyField(City, through='TripCity')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    price = models.PositiveBigIntegerField(null=True)


class TripCity(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=50)
