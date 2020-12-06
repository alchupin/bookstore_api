import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.user_staff = User.objects.create(username='test_staff_username', is_staff=True)
        self.book_1 = Book.objects.create(name='Clean coder', price=500.00, author='author_1', owner=self.user)
        self.book_2 = Book.objects.create(name='Clean code', price=600.00, author='author_2')
        self.book_3 = Book.objects.create(name='Code complete author_1', price=1000.00, author='author_3')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'author_1'})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.count())
        url = reverse('book-list')
        data = {
            "name": "Ulysses",
            "price": "350.00",
            "author": "James Augustine Aloysius Joyce"
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "400.00",
            "author": self.book_1.author
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(400, self.book_1.price)

    def test_update_not_owner(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "400.00",
            "author": self.book_1.author
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')},
                         response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(500, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "400.00",
            "author": self.book_1.author
        }
        self.client.force_login(self.user_staff)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(400, self.book_1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.count())


class BookRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.user_staff = User.objects.create(username='test_staff_username', is_staff=True)
        self.book_1 = Book.objects.create(name='Clean coder', price=500.00, author='author_1')
        self.book_2 = Book.objects.create(name='Clean code', price=600.00, author='author_2')
        self.book_3 = Book.objects.create(name='Code complete', price=1000.00, author='author_3')

    def test_like_bookmarks(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {"like": True}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {"in_bookmarks": True}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)
