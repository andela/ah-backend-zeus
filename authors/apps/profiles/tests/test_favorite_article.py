from .base_test import BaseTest
from rest_framework import status

class TestfavoriteArticle(BaseTest):

    def test_favorite_article(self):
        article = self.client.post('/api/articles/', data = self.new_article,format='json')
        slug = self.get_slug( article)
        response = self.client.put('/api/users/article/favorite/{}'.format(slug))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_favorite_article_which_doesnot_exist(self):
        response = self.client.put('/api/users/article/favorite/best-43hbc',format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_unfavorite_article(self):
        article = self.client.post('/api/articles/', data = self.new_article,format='json')
        slug = self.get_slug( article)
        self.client.put('/api/users/article/favorite/{}'.format(slug))
        response = self.client.put('/api/users/article/favorite/{}'.format(slug))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_unfavorite_article_which_doesnot_exist(self):
        article = self.client.post('/api/articles/', data = self.new_article,format='json')
        slug = self.get_slug( article)
        self.client.put('/api/users/article/favorite/{}'.format(slug))
        response = self.client.put('/api/users/article/favorite/man-1628t492')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)