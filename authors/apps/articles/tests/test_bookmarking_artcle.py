from rest_framework import status
from .base_test import BaseTest


class TestBookMarking(BaseTest):

    def test_bookmark_article(self):

        posted_article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(posted_article)
        response = self.client.post(
                '/api/articles/bookmark/{}'.format(slug)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unbookmarking_article(self):

        posted_article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(posted_article)
        self.client.post(
                '/api/articles/bookmark/{}'.format(slug)
        )
        response = self.client.post(
                '/api/articles/bookmark/{}'.format(slug)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_bookmarking_article_which_doesnot_exist(self):
        posted_article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        response = self.client.post(
                '/api/articles/bookmark/best-of-the-best-1234ghj9'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_bookmarked_article(self):

        posted_article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(posted_article)
        self.client.post(
                '/api/articles/bookmark/{}'.format(slug)
        )
        response = self.client.get(
                '/api/articles/bookmark/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)