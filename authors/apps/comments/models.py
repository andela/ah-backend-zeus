from django.db import models
from django.utils import timezone
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class Comments(models.Model):
    """
    create model for comments
    """
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_body = models.TextField(null=False, blank=False, error_messages={
        "required": "Please input the comment"})

    created_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    def __str__(self):
        """
        It returns a string
        """
        return self.comment_body

    class Meta:

        ordering = ['created_at']


class Replies(models.Model):
    """
    create a model for replies to a comment
    """
    comment = models.ForeignKey(
        Comments,
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    author = models.ForeignKey(
        User,
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    reply_message = models.TextField(
        null=False, blank=False, error_messages={
            "required": "please input your reply"})

    created_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    def __str__(self):
        """
        It returns a string
        """
        return self.reply_message

    class Meta:

        ordering = ['created_at']
