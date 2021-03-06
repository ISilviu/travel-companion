from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import CommonOperationsMixin, UserAuthMixin

from ..models.user import User
from ..serializers.user import UserSerializer


class UserApiTests(UserAuthMixin, CommonOperationsMixin, APITestCase):
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
        # POST requests should be allowed with no authenticated user
        self.client.logout()
        response = self.client.post(self.url_base, data={
                                    'username': 'isilviu', 'password': 'hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_no_results(self):
        # As a default user is always inserted, we need to override this test.
        result = self.client.get(self.url_base)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.data), 1)

    def test_get_auth_token(self):
        user_data = {
            'username': 'isilviu',
            'password': 'hello'
        }
        self.client.post(self.url_base, data=user_data, format='json')
        response = self.client.post('/auth/', data=user_data, format='json')
        self.assertTrue(len(response.data['token']))