from django.db import models
from authors.apps.authentication.models import User
from authors.apps.core.models import TimestampedModel


class Article(TimestampedModel):
    """
    Create and return an `Article` with a title, description and body.
    """

    slug = models.SlugField(
        db_index=True,
        max_length=255,
        unique=True,
        default=False)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(
        'profiles.UserProfile',
        on_delete=models.CASCADE,
        related_name='articles')
    likes = models.IntegerField(
        db_index=True,
        default=False
    )
    dislikes = models.IntegerField(
        db_index=True,
        default=False
    )

    def __str__(self):
        return self.title


class Impressions(TimestampedModel):
    """
    Create an `Impression` with a slug, user details, likes and dislikes.
    """

    slug = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        to_field="slug",
        db_column="slug"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    likes = models.BooleanField(
        db_index=True,
        default=None
    )
    dislikes = models.BooleanField(
        db_index=True,
        default=None
    )

