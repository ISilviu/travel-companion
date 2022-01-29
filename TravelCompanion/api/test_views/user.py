
from rest_framework.test import APITestCase

from ddf import G

from ..models.user import User
from ..serializers.user import UserSerializer


class UserApiTests(APITestCase):
    test_model = User
    serializer_class = UserSerializer
    url_base = '/api/users/'

    def test_list(self):
        G(self.test_model, n=10)

        result = self.client.get(self.url_base)
        self.assertEqual(result.data, self.serializer_class(
            self.test_model.objects.all(), many=True).data)

    def test_retrieve(self):
        id = 5
        G(self.test_model, id=id)
        G(self.test_model, id=6)

        result = self.client.get(f'{self.url_base}{id}/')

        expected = self.serializer_class(
            self.test_model.objects.filter(id=id).first()).data
        self.assertEqual(result.data, expected)
