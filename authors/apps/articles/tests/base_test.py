from django.urls import path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from authors.apps.authentication.views import RegistrationAPIView, AccountVerified
from authors.apps.authentication.models import User
from authors.apps.authentication.backends import JWTAuthentication


class BaseTest(APITestCase):

    def setUp(self):
        self.slug = 0
        self.sg = 0
        self.user_data = {
            "user": {
                "username": "minime",
                "email": "alexkayabula@gmail.com",
                "password": "W123456/78"}}
        self.url = reverse("registration")
        self.client = APIClient()
        self.client.post(self.url, self.user_data, format='json')
        self.request = APIRequestFactory().post(
            reverse("registration")
        )

        self.new_article = {
            "article": {
                "title": "How to fight dragons 8",
                "description": "Ever wonder jckvlahvhow?",
                "body": "You have kenglto believe",
                "tags": ["santa", "dorin"]
            }
        }

        self.update_article = {
            "article": {
                "title": "How to fight dragons 8",
                "description": "Ever wonder jckvlahvhow?",
                "body": "You have kenglto believe"
            }
        }

        self.article_without_title = {
            "article": {
                "description": "Ever wonder jckvlahvhow?",
                "body": "You have kenglto believe"
            }
        }

        self.rate_article = {
            'rating': 5
        }

        user = User.objects.get()
        request = self.request
        token, uid = RegistrationAPIView.generate_token(user, request)
        response = self.account_verification(token, uid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        self.assertTrue(user.is_verified)

        response = self.client.post(
            '/api/users/login/',
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.login_token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.login_token
        )

    def account_verification(self, token, uid):
        request = APIRequestFactory().get(
            reverse("verify_account", kwargs={"token": token, "uid": uid})
        )
        verify = AccountVerified.as_view()
        response = verify(request, token=token, uid=uid)
        return response

    def get_slug(self, response=[]):
        self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        response = self.client.get('/api/articles/', format='json')
        for i in response.data['results']:
            self.slug = i['slug']
        return self.slug
