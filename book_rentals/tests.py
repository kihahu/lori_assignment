from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import force_authenticate
import json

from .models import Book_Rental
from books.models import Book
from users.models import CustomUser
# Create your tests here.

User = get_user_model()

class BookRentalsModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
                            name="BookTest",
                            description = 'Description Test',
                            author = "Author Test",
                            )

        self.book2 = Book.objects.create(
                            name="BookTest2",
                            description = 'Description Test',
                            author = "Author Test",
                            )

        self.user = CustomUser.objects.create_user(
                            'test_username', 
                            'test_username@example.com', 
                            'da_password'
                            )
        
        self.book_rentals = Book_Rental.objects.create(
                            user=self.user, 
                            book=self.book
                            )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def create_book_rentals(self, book, user):
        book_rental = Book_Rental.objects.create(book=book, user=user)
        return book_rental
    

    def test_create_book_rental(self):
        book_rental = self.create_book_rentals(self.book, self.user)
        self.assertTrue(isinstance(book_rental, Book_Rental))
        self.assertEqual(book_rental.__str__(), str(book_rental.ref))
        
    
    def test_get_book_rentals_api(self):
        request = self.client.get('/api/books_rentals/')
        self.assertEqual(request.status_code, 200)


    def test_get_user_book_rentals_api(self):
        request = self.client.get('/api/book_rentals/customer/')
        self.assertEqual(request.status_code, 200)


    def test_get_book_rental_api(self):
        request = self.client.get('/api/book_rentals/'+str(self.book.id)+'/')
        self.assertEqual(request.status_code, 200)


    def test_create_Book_rentals_api(self):
        request = self.client.post('/api/book_rentals/create',
                                    json.dumps({
                                        'user_id':self.user.id,
                                        'book_id':self.book.id
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_update_book_rentals_api(self):
        request = self.client.put('/api/book_rentals/'+str(self.book_rentals.ref)+'/update',
                                    json.dumps({
                                        'user_id':self.user.id,
                                        'book_id':self.book.id,
                                        'status':2
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)

