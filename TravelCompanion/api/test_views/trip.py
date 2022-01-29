
from rest_framework.test import APITestCase
from rest_framework import status

from .mixins import CommonOperationsMixin

from ..models.trip import Trip
from ..models.user import User
from ..models.city import City
from ..serializers.trip import ReadonlyTripSerializer

from ddf import G


class TripApiTests(CommonOperationsMixin, APITestCase):
    test_model = Trip
    serializer_class = ReadonlyTripSerializer
    url_base = '/api/trips/'

    def test_create_trip_successful(self):
        user = G(User, username='the_bat',
                 first_name='Christian', last_name='Bale')
        user2 = G(User, username='tc', first_name='Tom', last_name='Cruise')
        user3 = G(User, username='jake', first_name='Jake',
                  last_name='Gyllenhaal')

        cities = G(City, n=5)

        data = {
            'initiator': user.pk,
            'participants': [
                user2.pk,
                user3.pk,
            ],
            'cities': [{'city': city.id, 'flight_number': city.id + 1} for city in cities],
            'start_date': '2022-01-19',
            'end_date': '2022-01-29',
            'price': 1000
        }

        response = self.client.post(self.url_base, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
