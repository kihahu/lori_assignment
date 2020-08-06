from django.contrib.auth import get_user_model
from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'name',
            'description',
            'author',
            'image',
        ]

