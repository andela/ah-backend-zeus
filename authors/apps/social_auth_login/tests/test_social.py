from rest_framework.test import APITestCase
from rest_framework import status


class SocialTests(APITestCase):

    def setUp(self):

        self.user_with_invalid_or_expired_google_token = {
            "user": {
                "auth_token": 'EAAcOwuP4YuoBAPopsu2H8eZCmV0d6ZCj3RKg2lAg1veQMJtwJTA6YTxP0cN4YAy8sZBqU7YLusM1Tdfs8WbmupC1gWtyEnmN7Cay6fuGNXrPZA6SkQ8qNTVVVuH685IV2SWrqTMhWeq7jdkPZAluuT3AKLd1mqXITCZCl37QZCsuJyAZAg3gAJnqU0Fuyxc4ZBumoVR3ALPWfHQZDZD'
            }
        }

        self.user_with_valid_facebook_token = {
            "user": {
                "auth_token": 'EAAEqZBZB3JqBIBABN22cJF95aX34VWOqG86W1sfbzR5WHqrMBI77Wgw7oUTTEwc7vSv9S7yLhkLWuEZCmaS9SXoQRUpX0us5ECKOMiw7dhNjzBLZAfqM6pwzHQvBqCIPGepyjYkNrLNEViEFFxaLoKzUCFkj21D2weKAvvTOeZAZCGS4WTb0ZBS1eSnMNIZAN5yFhzOdjqZBSsd1ZATn0awXmJ'
            }
        }

        self.user_with_invalid_or_expired_facebook_token = {
            "user": {
                "auth_token": 'EAAcOwuP4YuoBAPopsu2H8eZCmV0d6ZCj3RKg2lAg1veQMJtwJTA6YTxP0cN4YAy8sZBqU7YLusM1Tdfs8WbmupC1gWtyEnmN7Cay6fuGNXrPZA6SkQ8qNTVVVuH685IV2SWrqTMhWeq7jdkPZAluuT3AKLd1mqXITCZCl37QZCsuJyAZAg3gAJnqU0Fuyxc4ZBumoVR3ALPWfHQZDZD'
            }
        }

        self.user_with_valid_twitter_token = {
            "user": {
                "auth_token": 'user_with_valid_twitter_token'
            }
        }

        self.user_with_invalid_or_expired_twitter_token = {
            "user": {
                "auth_token": 'EAAcOwuP4YuoBAPopsu2H8eZCmV0d6ZCj3RKg2lAg1veQMJtwJTA6YTxP0cN4YAy8sZBqU7YLusM1Tdfs8WbmupC1gWtyEnmN7Cay6fuGNXrPZA6SkQ8qNTVVVuH685IV2SWrqTMhWeq7jdkPZAluuT3AKLd1mqXITCZCl37QZCsuJyAZAg3gAJnqU0Fuyxc4ZBumoVR3ALPWfHQZDZD'
            }
        }

    def test_login_with_invalid_google_token(self):
        """
        Test if a user can login with an invalid or expired google token
        """

        response = self.client.post(
            "/api/social/auth/google/",
            self.user_with_invalid_or_expired_google_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.', str(
                response.data))

    def test_login_with_invalid_or_expired_google_token(self):
        """
        Test if a user can login with an invalid or expired google token
        """

        response = self.client.post(
            "/api/social/auth/google/",
            self.user_with_invalid_or_expired_google_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.', str(
                response.data))

    def test_login_with_invalid_facebook_token(self):
        """
        Test if a user can login with an invalid or expired facebook token
        """

        response = self.client.post(
            "/api/social/auth/facebook/",
            self.user_with_invalid_or_expired_facebook_token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.', str(
                response.data))

    def test_login_with_invalid_or_expired_facebook_token(self):
        """
        Test if a user can login with an invalid or expired facebook token
        """

        response = self.client.post(
            "/api/social/auth/facebook/",
            self.user_with_invalid_or_expired_facebook_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.', str(response.data))

    def test_login_with_invalid_or_expired_twitter_token(self):
        """
        Test if a user can login with an invalid or expired twitter token
        """

        response = self.client.post(
            "/api/social/auth/twitter/",
            self.user_with_invalid_or_expired_twitter_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'The token is invalid or expired. Please login again.', str(
                response.data))
