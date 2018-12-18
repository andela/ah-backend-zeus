from rest_framework.test import APIClient
from .base_test import BaseTest
from rest_framework import status


class TestTagArticle(BaseTest):
    def test_create_article_with_tags(self):
        reponse = self.client.post(
            '/api/articles/',
            data={
                "article": {
                    "title": "How to fight dragons 8",
                    "description": "Ever wonder jckvlahvhow?",
                    "body": "You have kenglto believe",
                    "tagList": ["dragons", "fight"]
                }
            },
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

