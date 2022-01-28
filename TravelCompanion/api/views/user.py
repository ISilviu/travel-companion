from django.contrib.auth.models import Group
from rest_framework import viewsets

from ..serializers.user import UserSerializer, GroupSerializer
from ..models.user import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('participating_trips', 'initiated_trips')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
