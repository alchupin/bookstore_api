from django.contrib import admin
from django.contrib.auth.models import User

from .models import Book, UserBookRelation


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price')




admin.site.register(Book, BookAdmin)


class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserBookRelation._meta.get_fields()]


admin.site.register(UserBookRelation, UserBookRelationAdmin)