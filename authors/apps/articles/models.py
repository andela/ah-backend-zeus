from django.db import models
from authors.apps.profiles.models import UserProfile
from authors.apps.core.models import TimestampedModel
from django.contrib.postgres.fields import ArrayField


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
    score = models.FloatField(default=0)
    images = ArrayField(models.URLField(max_length=255),default=list)

    def __str__(self):
        return self.title


class Rating(models.Model):
    """
    Model to store ratings for user created articles.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField()
