from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
import json
from rest_framework.reverse import reverse
from ..models import User
from ..views import RegistrationAPIView, AccountVerified


class ListUserFunctionalityTests(APITestCase):
    def setUp(self):
        self.user_data = {'user': {
            'username': 'Jack Sparrow',
            'email': 'sparrow@gmail.com',
            'password': 'SeaC4ptain' 
        }}
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

    def test_api_can_list_all_registered_users(self):
        resp = self.client.post('/api/users/login/', data=self.user_data, format='json')
        body = json.loads(resp.content)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + body['user']['token'])
        resp = self.client.get('/api/authors/')
        body = json.loads(resp.content)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(body['authors'][0]['username'], 'Jack Sparrow')
        self.assertEqual(body['authors'][0]['email'], 'sparrow@gmail.com')

