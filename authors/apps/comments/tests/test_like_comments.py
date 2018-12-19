from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from .test_comment_data import CommentTest


class Test_Impression(CommentTest):

    def test_add_like_impression(self, response=[]):
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        
        self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')

        response = self.client.get(
            '/api/{}/comments/'.format(slug),
            format='json')

        for i in response.data['comments']:
            self.id = i['id']
        id = self.id
        response1 = self.client.post('/api/comment/like/{}'.format(id), format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

    def test_add_like_impression_twice(self, response=[]):
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        
        self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')

        response = self.client.get(
            '/api/{}/comments/'.format(slug),
            format='json')

        for i in response.data['comments']:
            self.id = i['id']
        id = self.id
        self.client.post('/api/comment/like/{}'.format(id), format='json')
        response1 = self.client.post('/api/comment/like/{}'.format(id), format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
    
    def test_add_like_impression_doesnot_exist(self):
        id = 908766
        response1 = self.client.post('/api/comment/like/{}'.format(id), format='json')

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid pk \"908766\" - object does not exist.', str(response1.data))
