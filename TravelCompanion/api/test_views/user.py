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
        response = self.client.post(self.url_base, data={'username': 'isilviu'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_successful(self):
        response = self.client.post(self.url_base, data={'username': 'isilviu', 'password': 'hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_auth_token(self):
        pass


