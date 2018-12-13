from rest_framework.test import APIClient
from .test_comment_data import CommentTest
# from authors.apps.articles.tests.base_test import BaseTest
from rest_framework import status


class TestComment(CommentTest):

    def test_create_comment(self):
        """
           create a comment on an article
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        reponse = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

    def test_commenting_without_body(self):
        """
           tests for commenting on an article without comment body
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        reponse = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_missing_comment,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_comment_and_replies(self):
        """
           tests for getting all comments and replies on an article
        """

        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        reponse = self.client.get(
            '/api/{}/comments/'.format(slug),
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)

    def test_post__comment_non_existing_article(self):
        """
           tests for commenting a non existing article
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        reponse = self.client.get(
            '/api/ghfdghbbjb/comments/',
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment(self):
        """
           tests for updating a comment
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)

        created_comment = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        slug = self.get_slug(created_comment)

        comment_id = created_comment.data['id']

        update_comment = {"comment": {
            "comment_body": "woooow!"
        }}
        response = self.client.put(
            '/api/comment/{}/'.format(comment_id),
            data=update_comment,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reply_to_comment(self):
        """
           tests for replying to a comment
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        comment = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        slug = self.get_slug(comment)

        comment_id = comment.data['id']

        reponse = self.client.post(
            '/api/comment/{}/replies/'.format(comment_id),
            data=self.reply_comment,
            format='json')

        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

    def test_reply_without_reply_message(self):
        """
           reply to comment without reply message
        """
        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)
        comment = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        slug = self.get_slug(comment)
        comment_id = comment.data['id']

        reponse = self.client.post(
            '/api/comment/{}/replies/'.format(comment_id),
            data=self.reply_missing_body,
            format='json')
        self.assertEqual(reponse.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_reply(self):
        """
          update reply
        """

        article = self.client.post(
            '/api/articles/',
            data=self.new_article,
            format='json')
        slug = self.get_slug(article)

        created_comment = self.client.post(
            '/api/{}/comments/'.format(slug),
            data=self.post_comment,
            format='json')
        slug = self.get_slug(created_comment)
        comment_id = created_comment.data['id']
        created_reply = self.client.post(
            '/api/comment/{}/replies/'.format(comment_id),
            data=self.reply_comment,
            format='json')

        slug = self.get_slug(created_reply)
        reply_id = created_reply.data['id']

        upate_reply = {"reply": {
            "reply_message": "hehehh that is nice"
        }}

        response = self.client.put(
            '/api/comment/replies/{}/'.format(reply_id),
            data=upate_reply,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
