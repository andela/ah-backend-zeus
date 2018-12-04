from rest_framework.test import APITestCase
from rest_framework import status


class TestUserProfile(APITestCase):
    def setUp(self):
        self.reg_user=0

    def test_get_a_list_of_userprofiles(self):
        response = self.client.get('/api/users/profiles',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_update_profile(self):
        data = {"user": {"username": "peter", "email": "peter@gmail.com", "password": "Peter1234.@"}}
        update_data = {
            "photo": "",
            "bio": "I have been a programmer since 1995",
            "fun_fact": "eating"
        }
        
        self.client.post('/api/users/', data, format='json')
        usr = self.client.get('/api/users/profiles').json()
        for u in usr:
            self.reg_user = u['user']

        response = self.client.put('/api/users/profiles/{}'.format(self.reg_user) + '/', update_data, format ='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

