
from rest_framework.test import APITestCase

from .mixins import ReadonlyOperationsTestsMixin

from ..models.city import City
from ..serializers.city import CitySerializer

class CityApiTests(ReadonlyOperationsTestsMixin, APITestCase): 
    test_model = City
    serializer_class = CitySerializer
    url_base = '/api/cities/'