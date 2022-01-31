
import datetime
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .mixins import CommonOperationsMixin

from ..models.trip import Trip, TripCity
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
            'participants': [],
            'cities': [],
            'start_date': '2022-01-19',
            'end_date': '2022-01-29',
            'price': 1000
        }

        data_with_participants = {
            **data,
            'participants': [user2.pk, user3.pk]
        }
        data_with_cities = {
            **data,
            'cities': [{'city': city.id, 'flight_number': city.id + 1} for city in cities]
        }
        data_with_both = {
            **data,
            'participants': [user2.pk, user3.pk],
            'cities': [{'city': city.id, 'flight_number': city.id + 1} for city in cities]
        }

        for data_set in [data, data_with_participants, data_with_cities, data_with_both]:
            response = self.client.post(
                self.url_base, data=data_set, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_trip_missing_fields(self):
        data = {
            'participants': [],
            'cities': [],
            'start_date': '2022-01-19',
            'end_date': '2022-01-29',
            'price': 1000
        }

        data_no_participants = {**data, 'initiator': 1}
        del data_no_participants['participants']

        data_no_cities = {**data, 'initiator': 1}
        del data_no_cities['cities']

        data_price_string = {**data, 'initiator': 1, 'price': '1000'}

        for data_set in [data, data_no_participants, data_no_cities, data_price_string]:
            response = self.client.post(
                self.url_base, data=data_set, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_start_after_end(self):
        data = {
            'initiator': 1,
            'participants': [],
            'cities': [],
            'start_date': '2022-01-30',
            'end_date': '2022-01-29',
            'price': 1000
        }

        response = self.client.post(
            self.url_base, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_cities(self):
        initiator = G(User)

        today = timezone.now()
        in_two_days = today + datetime.timedelta(days=2)

        trip = G(Trip, initiator=initiator, start_date=today,
                 end_date=in_two_days, price=100)
        cities = G(City, n=3)

        data = {
            'cities': [{'city': city.pk, 'flight_number': city.pk + 1} for city in cities]
        }

        response = self.client.patch(
            f'{self.url_base}{trip.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        trip = ReadonlyTripSerializer(
            Trip.objects.prefetch_related('cities').filter(id=trip.pk), many=True).data

        for index, city in enumerate(cities):
            persisted_city = trip[0]['cities'][index]['city']
            self.assertEqual(city.pk, persisted_city['id'])

    def test_get_trip_cities(self):
        initiator = G(User)

        today = timezone.now()
        in_two_days = today + datetime.timedelta(days=2)

        [city1, city2] = G(City, n=2)
        trip = G(Trip, initiator=initiator, start_date=today,
                 end_date=in_two_days, price=100)

        response = self.client.get(f'{self.url_base}{trip.pk}/cities/')
        self.assertEqual(len(response.data['cities']), 0)

        G(TripCity, trip=trip, city=city1, flight_number=50)
        G(TripCity, trip=trip, city=city2, flight_number=150)

        response = self.client.get(f'{self.url_base}{trip.pk}/cities/')
        self.assertEqual(len(response.data['cities']), 2)

    def test_update_trip_details(self):
        initiator = G(User)

        today = timezone.now()
        in_two_days = today + datetime.timedelta(days=2)

        [city1, city2] = G(City, n=2)
        trip = G(Trip, initiator=initiator, start_date=today,
                 end_date=in_two_days, price=100)
        G(TripCity, trip=trip, city=city1, flight_number=50)
        G(TripCity, trip=trip, city=city2, flight_number=150)

        expected_date = datetime.datetime(2025, 1, 29).date()
        end_date_data = {'end_date': expected_date.strftime("%Y-%m-%d")}

        self.client.patch(
            f'{self.url_base}{trip.pk}/', data=end_date_data, format='json')
        self.assertTrue(Trip.objects.get(pk=trip.pk).end_date == expected_date)

        initiator = G(User, username='tc')
        self.client.patch(
            f'{self.url_base}{trip.pk}/', data={'initiator': initiator.pk}, format='json')
        self.assertEqual(Trip.objects.get(pk=trip.pk).initiator.username, 'tc')
