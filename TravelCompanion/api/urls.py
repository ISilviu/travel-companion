from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()

# routes will go here


urlpatterns = [
    path('', include(router.urls)),
]