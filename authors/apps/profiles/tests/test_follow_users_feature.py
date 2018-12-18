from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from authors.apps.authentication.models import User
from authors.apps.authentication.views import RegistrationAPIView, AccountVerified
from django.urls import reverse
from rest_framework import status


class FollowUsersTests(APITestCase):
    def setUp(self):
        self.user1 = {'user': {
            'username': 'Jack Sparrow',
            'email': 'jacksparrow@gmail.com',
            'password': 'J4ckSparrow'
        }}
        self.user2 = {'user': {
            'username': 'Thor',
            'email': 'ragnarok@thor.com',
            'password': '4Sgardian'
        }}
        self.client.post('/api/users/', data=self.user1, format='json')
        self.verify_account(self.user1['user']['username'])
        self.client.post('/api/users/', data=self.user2, format='json')
        self.verify_account(self.user2['user']['username'])
        response = self.client.post('/api/users/login/', self.user1, format='json')
        self.auth_header_1 = 'Bearer {}'.format(response.data['token'])
        response = self.client.post('/api/users/login/', self.user2, format='json')
        self.auth_header_2 = 'Bearer {}'.format(response.data['token'])
    
    def verify_account(self, username):
        user = User.objects.get(username=username)
        request = APIRequestFactory().post(reverse('registration'))
        token, uid = RegistrationAPIView.generate_token(user, request)
        response = APIRequestFactory().get(
            reverse('verify_account', kwargs={'token': token, 'uid': uid})
        )
        verify = AccountVerified.as_view()
        response = verify(response, token=token, uid=uid)
        self.assertEqual(response.status_code, 200)

    def test_user_can_follow_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_1)
        response = self.client.post(
            '/api/profiles/{}/follows/'.format(self.user2['user']['username']), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['following'])
    
    def test_user_cannot_follow_own_self_or_another_user_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_2)
        response = self.client.post(
            '/api/profiles/{}/follows/'.format(self.user2['user']['username']), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
        response = self.client.post(
            '/api/profiles/{}/follows/'.format(self.user1['user']['username']), format='json'
        )
        response = self.client.post(
            '/api/profiles/{}/follows/'.format(self.user1['user']['username']), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
    
    def test_user_can_unfollow_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_1)
        response = self.client.post(
            '/api/profiles/{}/follows/'.format(self.user2['user']['username']), format='json'
        )
        response = self.client.delete(
            '/api/profiles/{}/follows/'.format(self.user2['user']['username']), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_user_cannot_unfollow_a_user_they_are_not_following(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_1)
        response = self.client.delete(
            '/api/profiles/{}/follows/'.format(self.user1['user']['username']), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
    
    def test_api_can_return_list_of_followings_for_a_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_2)
        response = self.client.get(
            '/api/profiles/{}/follows/'.format(self.user1['user']['username'], format='json')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('following' in response.data)
    
    def test_api_can_return_list_of_followers_for_a_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_1)
        response = self.client.get(
            '/api/profiles/{}/followers/'.format(self.user2['user']['username'], format='json')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('followers' in response.data)
