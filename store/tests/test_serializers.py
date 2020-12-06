from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Clean coder', price=500.00, author='Robert C. Martin')
        self.book_2 = Book.objects.create(name='Clean code', price=600.00, author='Robert C. Martin')
        self.book_3 = Book.objects.create(name='Code complete', price=1000.00, author='Steve McConnell')

    def test_ok(self):
        data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Clean coder',
                'price': '500.00',
                'author': 'Robert C. Martin'
            },
            {
                'id': self.book_2.id,
                'name': 'Clean code',
                'price': '600.00',
                'author': 'Robert C. Martin'
            },
            {
                'id': self.book_3.id,
                'name': 'Code complete',
                'price': '1000.00',
                'author': 'Steve McConnell'
            }
        ]
        print(data)
        print(expected_data)

        self.assertEqual(expected_data, data)
