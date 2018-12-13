from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status


class TestRatings(BaseTest):
    def test_api_can_rate_an_article(self):
        slug = self.get_slug()
        response = self.client.post(
            '/api/articles/{}/ratings/'.format(slug),
            data=self.rate_article, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_api_returns_404_for_non_existent_slug(self):
        response = self.client.post(
            '/api/articles/slug/ratings/',
            data=self.rate_article,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_api_returns_error_for_ratings_not_from_1_to_5(self):
        slug = self.get_slug()
        response = self.client.post(
            '/api/articles/{}/ratings/'.format(slug),
            data={'rating': -3}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
