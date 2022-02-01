from django.db import models


class City(models.Model):
    """
    The city model, consisting of a single field, its name.
    It represents destinations for trips.
    """
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name
