from django.urls import include, path
from rest_framework import routers

from .views.trip import TripViewSet
from .views.user import UserViewSet
from .views.city import CityViewSet

app_name = 'api'

router = routers.DefaultRouter()

# The application routes
router.register('trips', TripViewSet)
router.register('users', UserViewSet)
router.register('cities', CityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
