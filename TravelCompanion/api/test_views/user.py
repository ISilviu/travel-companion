from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import CommonOperationsMixin

from ..models.user import User
from ..serializers.user import UserSerializer


class UserApiTests(CommonOperationsMixin, APITestCase):
    """
    Tests for the /users endpoint.
    """
    test_model = User
    serializer_class = UserSerializer
    url_base = '/api/users/'

    def test_create_no_password(self):
        response = self.client.post(
            self.url_base, data={'username': 'isilviu'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_successful(self):
        response = self.client.post(self.url_base, data={
                                    'username': 'isilviu', 'password': 'hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def _retrieve_auth_token(self):
        user_data = {
            'username': 'isilviu',
            'password': 'hello'
        }
        self.client.post(self.url_base, data=user_data, format='json')
        response = self.client.post('/auth/', data=user_data, format='json')
        return response.data['token']

    def test_get_auth_token(self):
        token = self._retrieve_auth_token()
        self.assertTrue(len(token))

    def test_access_secured_route(self):
        response = self.client.get('/api/trips/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = self._retrieve_auth_token()
        response = self.client.get(
            '/api/trips/', format='json', **{'HTTP_AUTHORIZATION': f'Token {token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
