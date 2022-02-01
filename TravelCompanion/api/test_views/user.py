
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
