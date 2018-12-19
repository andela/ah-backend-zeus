from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status


class ReportArticle(BaseTest):

    def test_user_can_report_an_article(self):
        created_article = self.client.post(
            '/api/articles/', data=self.new_article, format='json')
        slug = self.get_slug(created_article)
        data = {"reason" : "This article is plagiarised"}
        response = self.client.post('/api/{}/report_article'.format(slug), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response1 = self.client.post('/api/{}/report_article'.format(slug), data=data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertIn("You have already reported this Article" , str(response1.data))
        
    def test_user_reporting_non_existant_article(self):
        data = {"reason" : "This article is plagiarised"}
        response = self.client.post('/api/{}/report_article'.format(20), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Article does not exist!" , str(response.data))
