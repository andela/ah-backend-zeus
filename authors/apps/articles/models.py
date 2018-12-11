from django.db import models
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

    def __str__(self):
        return self.title
