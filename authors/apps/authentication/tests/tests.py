from django.urls import path, reverse
from rest_framework.test import APITestCase, APIRequestFactory
from ..views import RegistrationAPIView, AccountVerified
from rest_framework import status
from ..models import User

class Authentication(APITestCase):

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

    def test_for_missing_username(self):
        """
        Method for testing if there is a missing username during registration.
        """
        data = {"user": { "username":"", "email": "lindsey@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please the username should be at least 4 characters long and above", str(response.data))

    def test_for_missing_email(self):
        """
        Method for testing if there is a missing email during registration.
        """
        data = {"user": { "username":"lindsey", "email": "", "password":"lindseypatra"}}
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please enter a valid email address", str(response.data))

    def test_login(self):
        """
        Method for logging in a  an existing user
        """
        data = {"user": { "username":"lindsey", "email": "lindsey@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/',data, format='json')
        data = {"user": { "email": "lindsey@gmail.com", "password":"Lindseypatra1/"}}
        response = self.client.post('/api/users/login/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email,"lindsey@gmail.com" )

    def test_login_with_non_existing_user(self):
        data = {"user": { "email": "mose@gmail.com", "password":"linds2456"}}
        response = self.client.post('/api/users/login/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with this email and password was not found.", str(response.data))
        