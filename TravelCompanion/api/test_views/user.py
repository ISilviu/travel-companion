
from rest_framework.test import APITestCase

from .mixins import ReadonlyOperationsTestsMixin

from ..models.user import User
from ..serializers.user import UserSerializer


class UserApiTests(ReadonlyOperationsTestsMixin, APITestCase):
    test_model = User
    serializer_class = UserSerializer
    url_base = '/api/users/'
