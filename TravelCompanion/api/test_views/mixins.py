from ddf import G
from django.db import models
from rest_framework import serializers, status

class ReadonlyOperationsTestsMixin:
    test_model: models.Model = None
    serializer_class: serializers.Serializer = None
    url_base: str = None

    def test_list(self):
        G(self.test_model, n=10)

        result = self.client.get(self.url_base)
        self.assertEqual(result.data, self.serializer_class(
            self.test_model.objects.all(), many=True).data)

    def test_list_no_results(self):
        result = self.client.get(self.url_base)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.data), 0)

    def test_retrieve(self):
        id = 5
        G(self.test_model, id=id)
        G(self.test_model, id=6)

        result = self.client.get(f'{self.url_base}{id}/')

        expected = self.serializer_class(
            self.test_model.objects.filter(id=id).first()).data
        self.assertEqual(result.data, expected)

    def test_retrieve_not_found(self):
        result = self.client.get(f'{self.url_base}5/')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    