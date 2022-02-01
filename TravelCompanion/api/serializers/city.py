from rest_framework import serializers
from ..models.city import City


class CitySerializer(serializers.ModelSerializer):
    """
    The City model serializer, used for all the CRUD methods the endpoint supports.
    """
    class Meta:
        model = City
        fields = ['id', 'name']
