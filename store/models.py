from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='books_created_by_user')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books_read_by_user')

    def __str__(self):
        return f'Title: {self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Awful'),
        (2, 'Bad'),
        (3, 'So-so'),
        (4, 'Good'),
        (5, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.SmallIntegerField(choices=RATE_CHOICES, null=True)
