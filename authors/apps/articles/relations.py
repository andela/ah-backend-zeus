from rest_framework import serializers

from .models import Tag


class TagRelatedField(serializers.RelatedField):
    """
    A Special Serializer field for Tags.
    If a user tags an article with an non existing tag, that new tag will also be created on article creation
    """

    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        return tag

    def to_representation(self, value):
        """
        Return a tag property
        """
        return value.tag
