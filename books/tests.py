import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import force_authenticate
from users.models import CustomUser
from books.models import Book


# Create your tests here.
class BookModelTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(
            'test_username', 
            'test_username@example.com', 
            'da_password',
        )
        self.book = Book.objects.create(
                        name="BookTest",
                        description = 'Description Test',
                        author = "Author Test",
                        book_type = 1
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def create_Book(self, name, description, author, book_type):
        return Book.objects.create(
                                name = name,
                                description = description,
                                author = author,
                                book_type = book_type
                                )


    def test_book_creation(self):
        f = self.create_Book(
                            'Book1',
                            'Description Test',
                            'Author Test',
                            1
                        )
        self.assertTrue(isinstance(f, Book))
        self.assertTrue(f.name =="Book1")
        self.assertEqual(f.__str__(), f.name)


    def test_creation_book_nonunique_name(self):
        f = self.create_Book(
                            'Book1',
                            'Description Test',
                            'Author Test',
                            1
                        )
        with self.assertRaises(IntegrityError):
            self.create_Book(
                            'Book1',
                            'Description Test',
                            'Author Test',
                            1
                        ).full_clean()

    
    def test_creation_Book_invalid_name(self):
        with self.assertRaises(ValidationError):
            self.create_Book(
                            '',
                            'Description Test',
                            'Author Test',
                            1
                        ).full_clean()


    def test_creation_book_invalid_description(self):
        with self.assertRaises(ValidationError):
            self.create_Book(
                            'Book123456789',
                            '',
                            'Author Test',
                            1
                        ).full_clean()
            
    
    def test_creation_book_invalid_author(self):
        with self.assertRaises(ValidationError):
            self.create_Book(
                            'Book123456789',
                            'Description Test',
                            '',
                            1
                        ).full_clean()


    def test_get_books_api(self):
        request = self.client.get('/api/v1/books/')
        self.assertEqual(request.status_code, 200)

    
    def test_create_book_api(self):
        request = self.client.post('/api/v1/books/',
                                    json.dumps({
                                        'name':"BookT12",
                                        'description':'Description Test',
                                        'author':"Author"
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_get_book_api(self):
        request = self.client.get('/api/v1/books/'+str(self.book.id))
        self.assertEqual(request.status_code, 200)

    
    def test_delete_Book_api(self):
        request = self.client.delete('/api/v1/books/'+str(self.book.id)+'/delete')
        self.assertEqual(request.status_code, 204)

    
    def test_update_book_api(self):
        request = self.client.put('/api/v1/books/'+str(self.book.id)+'/update',
                                    json.dumps({
                                        'name':"BookT12",
                                        'description':'Description Update',
                                        'author':"Author Update"
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)
        
        
    def test_get_books_api(self):
        request = self.client.get('/api/v2/books/')
        self.assertEqual(request.status_code, 200)

    
    def test_create_book_api(self):
        request = self.client.post('/api/v2/books/',
                                    json.dumps({
                                        'name':"BookT12",
                                        'description':'Description Test',
                                        'author':"Author",
                                        'book_type':1
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 201)


    def test_get_book_api(self):
        request = self.client.get('/api/v2/books/'+str(self.book.id))
        self.assertEqual(request.status_code, 200)

    
    def test_delete_Book_api(self):
        request = self.client.delete('/api/v2/books/'+str(self.book.id)+'/delete')
        self.assertEqual(request.status_code, 204)

    
    def test_update_book_api(self):
        request = self.client.put('/api/v2/books/'+str(self.book.id)+'/update',
                                    json.dumps({
                                        'name':"BookT12",
                                        'description':'Description Update',
                                        'author':"Author Update",
                                        'book_type': 1
                                        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(request.status_code, 200)
