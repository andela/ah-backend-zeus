from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status



class TestSharing(BaseTest):
    def test_api_can_share_an_article_on_facebook(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        response = self.client.post(
            '/api/articles/{}/facebook/'.format(slug),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_share_an_article_with_facebook_with_wrong_slug(self):
        response = self.client.post(
            '/api/articles/slug/facebook/',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_api_can_share_an_article_on_twitter(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        response = self.client.post(
            '/api/articles/{}/twitter/'.format(slug),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_share_an_article_with_twitter_with_wrong_slug(self):
        response = self.client.post(
            '/api/articles/slug/twitter/',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_api_can_share_an_article_with_email(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        response = self.client.post(
            '/api/articles/{}/email/'.format(slug),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_share_an_article_with_email_with_wrong_slug(self):
        response = self.client.post(
            '/api/articles/slug/email/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



