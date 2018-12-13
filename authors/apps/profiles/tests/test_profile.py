from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import path, reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from authors.apps.authentication.views import RegistrationAPIView, AccountVerified
from authors.apps.authentication.models import User
from authors.apps.authentication.backends import JWTAuthentication


class TestUserProfile(APITestCase):
     
    def setUp(self):
        self.user_data = {"user": { "username":"minime", "email": "alexkayabula@gmail.com", "password":"W123456/78"}}
        self.url = reverse("registration")
        self.client = APIClient()
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

        response = self.client.post('/api/users/login/',self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.login_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.login_token)
       
       

    def account_verification(self, token, uid):
        request = APIRequestFactory().get(
            reverse("verify_account", kwargs={"token": token, "uid":uid})
        )
        verify = AccountVerified.as_view()
        response = verify(request, token=token, uid=uid)
        return response

    def test_get_a_list_of_userprofiles(self): 
        

        response = self.client.get('/api/users/profiles', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
    

    def test_update_profile(self):
        update_data = {"bio":"I have been doing programming since 1995",
                        "fun_fact":"I love dancing"
        }

        response = self.client.put('/api/users/profiles/', update_data, format ='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)