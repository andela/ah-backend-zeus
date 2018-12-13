from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status


class Test_Impression(BaseTest):

    def test_add_like_impression(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        reponse = self.client.post(
            '/api/articles/like/{}'.format(slug),
            data=self.new_article,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

    def test_add_dislike_impression(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        reponse = self.client.post(
            '/api/articles/dislike/{}'.format(slug),
            data=self.article_without_title,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

    def test_user_is_neutral_after_liking_twice(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        self.client.post(
            '/api/articles/like/{}'.format(slug),
            data=self.new_article,
            format='json')
        self.client.post(
            '/api/articles/like/{}'.format(slug),
            data=self.new_article,
            format='json')
        reponse = self.client.get('/api/articles/', format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)


    def test_user_can_not_dislike_and_like_an_article(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        self.client.post(
            '/api/articles/dislike/{}'.format(slug),
            data=self.new_article,
            format='json')
        self.client.post(
            '/api/articles/like/{}'.format(slug),
            data=self.new_article,
            format='json')
        reponse = self.client.get('/api/articles/', format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)

    
    def test_user_can_not_like_and_dislike_an_article(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)

        self.client.post(
            '/api/articles/like/{}'.format(slug),
            data=self.new_article,
            format='json')
        self.client.post(
            '/api/articles/dislike/{}'.format(slug),
            data=self.new_article,
            format='json')
        reponse = self.client.get('/api/articles/', format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)
