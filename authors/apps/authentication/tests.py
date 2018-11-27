from django.urls import reverse, path
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class Authentication(APITestCase):
     
    def test_for_new_user(self):
    #    url = reverse('signup')
       data = {"user": { "username":"lindsey", "email": "lindsey@gmail.com", "password":"lindseypatra"}}
       response = self.client.post('/api/users/' ,data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_login(self):
        # url = reverse('signup')
        data = {"user": { "username":"lindsey", "email": "lindsey@gmail.com", "password":"lindseypatra"}}
        response = self.client.post('/api/users/',data, format='json')
        # url = reverse('login')
        data = {"user": { "email": "lindsey@gmail.com", "password":"lindseypatra"}}
        response = self.client.post('/api/users/login/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email,"lindsey@gmail.com" )