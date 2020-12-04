from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Clean coder', price=500.00)
        book_2 = Book.objects.create(name='Clean code', price=600.00)
        book_3 = Book.objects.create(name='Code complete', price=1000.00)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([book_1, book_2, book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)