from rest_framework import serializers, status
from django.urls import path, reverse
from rest_framework.test import APITestCase, APIRequestFactory
from authors.apps.authentication.serializers import RegistrationSerializer
from ..views import RegistrationAPIView, AccountVerified
from ..backends import JWTAuthentication
from ..models import User, UserManager

class AuthTestCase(APITestCase):
    '''Test JWT authentication for ah-backend-zues''' 

    def setUp(self):
        self.user_data = {"user": { "username":"minime", "email": "alexkayabula@gmail.com", "password":"W123456/78"}}
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
        user = User.objects.get()
        self.assertTrue(user.is_verified) 

    def account_verification(self, token, uid):
        request = APIRequestFactory().get(
            reverse("verify_account", kwargs={"token": token, "uid":uid})
        )
        verify = AccountVerified.as_view()
        response = verify(request, token=token, uid=uid)
        return response 

    def test_token_received_after_successful_registration(self):
        """
        Test that a user will receive 
        a token after successfull registration
        """
        data = {
            "user": {
                "username": "eric",
                "email": "eric@gmail.com",
                "password": "Get/2015"
            }
        }                    
        response = self.client.post('/api/users/' ,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_received_after_successful_login(self):
        """
        Test that a user will receive 
        a token after successfull login
        """
        data = {
            "user": {
                "username": "eric",
                "email": "eric@gmail.com",
                "password": "Get/2015"
            }
        }
        response = self.client.post('/api/users/login/',self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        assert 'token' in response.data

    def test_user_can_get_current_user(self):
        """
        Test that a user will receive 
        a token after successfull login
        """
        data = {
            "user": {
                "username": "minime",
                "email": "alexkayabula@gmail.com",
                "password": "W123456/78"
            }
        }
        response = self.client.post('/api/users/',data, format='json')
        data = {
            "user": {
                "email": "alexkayabula@gmail.com",
                "password": "W123456/78"
            }
        }
        response = self.client.post('/api/users/login/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        assert 'token' in response.data
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer ' + response.data['token'])
        response = self.client.get('/api/user/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_wrong_token_header_prefix(self):
        """
        Test when wrong authoriation header
        prefix is entered
        """
        self.client.credentials(HTTP_AUTHORIZATION= 'hgfds ' + 'poiuytfd')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_for_invalid_token(self):
        """
        Test when an invalid 
        authorisation header is provided
        """
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + 'yyuug')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

    def test_no_token_in_header(self):
        """
        Test when no authorization token
        is entered in the header
        """
        self.client.credentials(HTTP_AUTHORIZATION= ' ' + 'shfdj')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
