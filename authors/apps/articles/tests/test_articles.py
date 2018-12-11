from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status


class Test_article(BaseTest):

    def test_create_articles(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

    def test_create_articles_without_title(self):

        reponse = self.client.post(
            '/api/articles/',
            data=self.article_without_title,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_articles(self):
        self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        reponse = self.client.get('/api/articles/', format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)

    def test_get_article_which_doesnot_exist(self):
        self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        reponse = self.client.get(
            '/api/articles/ft-bhj-bhnckdcnx-',
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        response = self.client.put(
            '/api/articles/{}'.format(slug),
            data=self.update_article,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_article(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        response = self.client.delete(
            '/api/articles/{}'.format(slug),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_article_that_doesnot_exist(self):
        self.client.post('/api/articles/', 
            data=self.new_article, format='json')

        response = self.client.delete(
            '/api/articles/blahblahblah',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    