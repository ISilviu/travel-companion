from django.urls import include, path
from rest_framework import routers

from .views.trip import TripViewSet
from .views.user import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()

# routes will go here
router.register('trips', TripViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
