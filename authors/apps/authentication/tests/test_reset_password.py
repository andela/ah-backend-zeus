from .base_test import BaseTest
from rest_framework import status


class TestRestPassWord(BaseTest):

    def test_reset_password(self):
        usr = {
            "user": {
                "username": "minime",
                "email": "alexkayabula@gmail.com",
                "password": "W123456/78"}}
        self.client.post('/api/users/password_reset/',data = usr,format = 'json')
        reset_data = {
            "user": {
                "username": "minime",
                "email": "alexkayabula@gmail.com",
                "password": "Whbdc^734"}}
        response = self.client.post('/api/users/password_reset/',data = reset_data ,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Check your email for the password reset link", str(response.data))
        
    
    def test_reset_password_with_missing_email(self):
        usr = {
            "user": {
                "username": "minime",
                "email": "",
                "password": "W123456/78"}}
        response = self.client.post('/api/users/password_reset/',data = usr,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_for_non_existant_user(self):
        reset_data = {
            "user": {
                "email": "nonexistant@gmail.com"}}
        response = self.client.post('/api/users/password_reset/', data = reset_data ,format = 'json')
        self.assertIn("User not found", str(response.data))
    