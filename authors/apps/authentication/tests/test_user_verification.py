from django.urls import path, reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from ..models import User
from django.core import mail
from rest_framework import serializers
from authors.apps.authentication.serializers import RegistrationSerializer
from datetime import datetime, timedelta
import jwt
from ..views import RegistrationAPIView, AccountVerified
from django.conf import settings

class TestUserVerification(APITestCase):

    def setUp(self):
        self.user_data = {"user": { "username":"lindsey", "email": "lindsey@gmail.com", "password":"Lindseypatra1/"}}
        self.url = reverse("registration")
        self.client.post(self.url, self.user_data, format='json')
        self.request = APIRequestFactory().post(
            reverse("registration")
        )
        user = User.objects.get()
        request = self.request
        token, uid = RegistrationAPIView.generate_token(user, request)
        response = self.account_verification(token, uid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =User.objects.get()
        self.assertTrue(user.is_verified)
    
    def account_verification(self, token, uid):
        request = APIRequestFactory().get(
            reverse("verify_account", kwargs={"token": token, "uid":uid})
        )
        verify = AccountVerified.as_view()
        response = verify(request, token=token, uid=uid)
        return response
    
    def test_for_new_user(self):
        """
        Method for testing registration of a new user.
        """
        data = {"user": { "username":"lindsey1", "email": "lindsey1@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn ("{'message': 'User successfully Registered, check your email and click the link to verify'}", str(response.data) )
    
    def test_login_unverified_user(self):
        """
        Method for testing logging in when user is un verified.
        """
        registration_data = {"user": { "username":"lindsey1", "email": "lindsey1@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/' ,registration_data, format='json')
        data = {"user": { "email": "lindsey1@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/login/',data, format='json')
        self.assertIn("This user has not been verified. Please signup or check your email and click the verification link", str(response.data))
    
    def test_token_received_after_successful_login(self):
        """
        Test that a user will receive 
        a token after successfull login
        """
        response = self.client.post('/api/users/login/',self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        assert 'token' in response.data
