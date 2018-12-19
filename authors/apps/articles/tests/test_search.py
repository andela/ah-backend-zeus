from rest_framework.test import APIClient
from rest_framework import status
from .base_test import BaseTest


class SearchTest(BaseTest):

    def test_search_article_by_author(self):
        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

        author = self.user_data['user']['username']

        response = self.client.get(
            '/api/articles/search/?author={}'.format(author))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_wrong_author(self):
        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

        author = self.user_data['user']['username']

        response = self.client.get(
            '/api/articles/search/?author=sam')
        self.assertTrue(response.data['errors'])
        self.assertEqual(response.status_code, 404)

    def test_search_article_by_title(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)
        title = self.new_article['article']['title']

        response = self.client.get(
            '/api/articles/search/?title={}'.format(title))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_keywords(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)
        keywords = self.new_article['article']['title']

        response = self.client.get(
            '/api/articles/search/?keyword={}'.format(keywords))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_title_and_author(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)
        title = self.new_article['article']['title']
        author = self.user_data['user']['username']
        response = self.client.get(
            '/api/articles/search/?title={}&author={}'.format(title,author))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_tag(self):
        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

        tags = self.new_article['article']['tags']

        response = self.client.get(
            '/api/articles/search/?tags={}'.format(tags))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_tag_and_author(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)
        tags = self.new_article['article']['tags']
        author = self.user_data['user']['username']
        response = self.client.get(
            '/api/articles/search/?tags={}&author={}'.format(tags,author))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_wrong_tag(self):
        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

        tags = self.new_article['article']['tags']

        response = self.client.get(
            '/api/articles/search/?tags=wbnbnbb')
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

        

    
        



    