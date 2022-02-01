
from rest_framework.test import APITestCase
from rest_framework import status

from .mixins import CommonOperationsMixin

from ..models.city import City
from ..serializers.city import CitySerializer

from ddf import G


class CityApiTests(CommonOperationsMixin, APITestCase):
    """
    Tests for the /cities endpoint.
    """
    test_model = City
    serializer_class = CitySerializer
    url_base = '/api/cities/'

    def test_create_success(self):
        data = {
            'name': 'New York'
        }

        response = self.client.post(self.url_base, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url_base)
        self.assertEqual(response.data, self.serializer_class(
            City.objects.all(), many=True).data)

    def test_create_duplicates(self):
        G(City, name='New York')

        response = self.client.post(
            self.url_base, {'name': 'New York'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        city = G(City, name='New York')
        city2 = G(City, name='Los Angeles')

        patch_args = {'path': f'{self.url_base}{city.pk}/',
                      'data': {'name': 'Detroit'}, 'format': 'json'}
        response = self.client.patch(**patch_args)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(City.objects.filter(name='Detroit').exists())

        # We can't have cities with the same name
        response = self.client.put(
            **{**patch_args, 'path': f'{self.url_base}{city2.pk}/', })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
