from django.urls import reverse, path
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User

class Authentication(APITestCase):
     
    

    def test_for_wrong_username(self):
        """
        Method for testing if there is a  wrong username during registration.
        """
        data = {"user": { "username" : "344samyu", "email" : "samrub@gmail.com", "password" : "Get/2018"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username should start with letters and sometimes include underscores and numbers", str(response.data))

    def test_for_missing_user_inputs(self):
        """
        Method for testing if there are no credentials provided during registration
        """
        
        response = self.client.post('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("input fields", str(response.data))

    def test_for_wrong_password(self):
        """
        Method for testing if there is wrong password provided during registration
        """
        data = {"user": { "username" : "samrub", "email" : "samrub@gmail.com", "password" : "dvhhshbdbbb"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self. assertIn("Weak password: password should contain at least 8 characters long ,capital letter and a number", str(response.data))

    def test_for_wrong_email(self):
        """
        Method for testing if there is invalid email  during registration.
        """
        data = {"user": { "username" : "samyu", "email" : "samrubgmail.com", "password" : "Get/2018"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please enter a valid email address", str(response.data))