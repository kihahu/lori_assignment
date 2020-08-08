from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json
from users.models import CustomUser
# Create your tests here.


class UserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            'test_username', 
            'test_username@example.com', 
            'da_password',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_create_username(self):
        self.assertTrue(isinstance(self.user, CustomUser))


    def test_api_can_list_all_user(self):
        response = self.client.get('/api/v1/accounts/')
        self.assertEqual(response.status_code, 200) 
        
        
    def test_api_can_get_a_user(self):
        response = self.client.get('/api/v1/accounts/'+str(self.user.id))
        self.assertEqual(response.status_code, 200) 


    def test_api_can_update_a_user(self):
        response = self.client.put('/api/v1/accounts/'+str(self.user.id)+'/update',
                                    json.dumps({
                                    "name": "Ahmed Yusuf",
                                    "phone": "0701874389",
                                    "address": "Test"}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200) 
        
        
    def test_api_invalid_user_update(self):
        response = self.client.put('/api/v1/accounts/'+str(self.user.id)+'/update',
                                    json.dumps({
                                    "name": "",
                                    "phone": "0701874389",
                                    "address": "Test"}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200) 


    def test_api_can_update_a_user__invalidphone(self):
        response = self.client.put('/api/v1/accounts/'+str(self.user.id)+'/update',
                                    json.dumps({
                                    "name": "Ahmed Yusuf",
                                    "phone": "07018743898909",
                                    "address": "Test"}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 400) 
        
        
    
