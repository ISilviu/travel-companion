from rest_framework.test import APITestCase
from rest_framework import status


class SecuredRoutesApiTests(APITestCase):
    def _retrieve_auth_token(self):
        user_data = {
            'username': 'user',
            'password': 'user'
        }
        self.client.post('/api/users/', data=user_data, format='json')
        response = self.client.post('/auth/', data=user_data, format='json')
        return response.data['token']

    def test_access_routes(self):
        app_routes = ['/api/cities/', '/api/trips/', '/api/users/']

        for route in app_routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            token = self._retrieve_auth_token()
            response = self.client.get(
                route, format='json', **{'HTTP_AUTHORIZATION': f'Token {token}'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)