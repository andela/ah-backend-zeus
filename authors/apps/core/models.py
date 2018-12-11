from django.db import models


class TimestampedModel(models.Model):
    """
    Adds a timestamp representing when the object was created
    and when that object was last updated.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
