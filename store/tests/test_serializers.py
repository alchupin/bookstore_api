from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Clean coder', price=500.00)
        book_2 = Book.objects.create(name='Clean code', price=600.00)
        book_3 = Book.objects.create(name='Code complete', price=1000.00)
        data = BookSerializer([book_1, book_2, book_3], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Clean coder',
                'price': '500.00'
            },
            {
                'id': book_2.id,
                'name': 'Clean code',
                'price': '600.00'
            },
            {
                'id': book_3.id,
                'name': 'Code complete',
                'price': '1000.00'
            },
        ]
        self.assertEqual(expected_data, data)
