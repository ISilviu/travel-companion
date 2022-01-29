
from rest_framework.test import APITestCase

from .mixins import CommonOperationsMixin

from ..models.trip import Trip
from ..serializers.trip import ReadonlyTripSerializer


class TripApiTests(CommonOperationsMixin, APITestCase):
    test_model = Trip
    serializer_class = ReadonlyTripSerializer
    url_base = '/api/trips/'
