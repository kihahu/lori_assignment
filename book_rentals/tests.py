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
                            book_type = 1
                            )

        self.book_2 = Book.objects.create(
                            name="BookTest2",
                            description = 'Description Test',
                            author = "Author Test",
                            book_type = 2
                            )
        
        self.book_3 = Book.objects.create(
                            name="BookTest3",
                            description = 'Description Test',
                            author = "Author Test",
                            book_type = 3
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
        
        self.book_rentals_2 = Book_Rental.objects.create(
                            user=self.user, 
                            book=self.book_2,
                            date_rented = '2020-08-01 20:08'
                            )
        
        self.book_rentals_3 = Book_Rental.objects.create(
                            user=self.user, 
                            book=self.book_3,
                            date_rented = '2020-08-01 20:08'
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
        request = self.client.get('/api/v1/book_rentals/')
        self.assertEqual(request.status_code, 200)


    def test_get_user_book_rentals_api(self):
        request = self.client.get('/api/v1/book_rentals/users/'+str(self.user.id))
        self.assertEqual(request.status_code, 200)


    def test_get_book_rental_api(self):
        request = self.client.get('/api/v1/book_rentals/'+str(self.book_rentals.ref))
        self.assertEqual(request.status_code, 200)


    def test_create_book_rentals_api(self):
        request = self.client.post('/api/v1/book_rentals/create',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_update_book_rentals_api(self):
        request = self.client.put('/api/v1/book_rentals/'+str(self.book_rentals.ref)+'/update',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id,
                                        'status':2
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)
        
    
    def test_delete_book_rental_api(self):
        request = self.client.delete('/api/v1/book_rentals/'+str(self.book_rentals.ref)+'/delete')
        self.assertEqual(request.status_code, 204)
        
    
    def test_book_rentals_balance_api(self):
        request = self.client.get('/api/v1/book_rentals/users/balance/'+str(self.user.id))
        request_data = json.loads(request.content)[0]
        self.assertEqual(request.status_code, 200)
        self.assertEqual('11', request_data.get('balance'))
        
        
    def test_get_book_rentals_api(self):
        request = self.client.get('/api/v2/book_rentals/')
        self.assertEqual(request.status_code, 200)


    def test_get_user_book_rentals_api(self):
        request = self.client.get('/api/v2/book_rentals/users/'+str(self.user.id))
        self.assertEqual(request.status_code, 200)


    def test_get_book_rental_api(self):
        request = self.client.get('/api/v2/book_rentals/'+str(self.book_rentals.ref))
        self.assertEqual(request.status_code, 200)


    def test_create_book_rentals_api(self):
        request = self.client.post('/api/v2/book_rentals/create',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_update_book_rentals_api(self):
        request = self.client.put('/api/v2/book_rentals/'+str(self.book_rentals.ref)+'/update',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id,
                                        'status':2
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)
        
    
    def test_delete_book_rental_api(self):
        request = self.client.delete('/api/v2/book_rentals/'+str(self.book_rentals.ref)+'/delete')
        self.assertEqual(request.status_code, 204)
        
        
    def test_book_rentals_balance_api_v2(self):
        request = self.client.get('/api/v2/book_rentals/users/balance/'+str(self.user.id))
        request_data = json.loads(request.content)[0]
        self.assertEqual(request.status_code, 200)
        self.assertEqual('24.0', request_data.get('balance'))
        
        
    def test_get_book_rentals_api(self):
        request = self.client.get('/api/v3/book_rentals/')
        self.assertEqual(request.status_code, 200)


    def test_get_user_book_rentals_api(self):
        request = self.client.get('/api/v3/book_rentals/users/'+str(self.user.id))
        self.assertEqual(request.status_code, 200)


    def test_get_book_rental_api(self):
        request = self.client.get('/api/v3/book_rentals/'+str(self.book_rentals.ref))
        self.assertEqual(request.status_code, 200)


    def test_create_book_rentals_api(self):
        request = self.client.post('/api/v3/book_rentals/create',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_update_book_rentals_api(self):
        request = self.client.put('/api/v3/book_rentals/'+str(self.book_rentals.ref)+'/update',
                                    json.dumps({
                                        'user':self.user.id,
                                        'book':self.book.id,
                                        'status':2
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)
        
    
    def test_delete_book_rental_api(self):
        request = self.client.delete('/api/v3/book_rentals/'+str(self.book_rentals.ref)+'/delete')
        self.assertEqual(request.status_code, 204)
        
        
    def test_book_rentals_balance_api_v2(self):
        request = self.client.get('/api/v3/book_rentals/users/balance/'+str(self.user.id))
        request_data = json.loads(request.content)[0]
        self.assertEqual(request.status_code, 200)
        self.assertEqual('24.5', request_data.get('balance'))
        
        

