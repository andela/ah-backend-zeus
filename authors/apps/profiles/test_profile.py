from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class TestUserProfile(APITestCase):

    def test_get_a_list_of_userprofiles(self):
        response = self.client.get('/api/users/profiles',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_profile(self):
        data={"user": { "username":"peter", "email": "peter@gmail.com", "password":"peter1234"}}
        update_data={
            "photo":"",
            "bio":"I have been a programmer since 1995",
            "fun_fact":"eating"
        }
        
        self.client.post('/api/users/',data,format='json')

        response = self.client.put('/api/users/profiles/3/edit',update_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

