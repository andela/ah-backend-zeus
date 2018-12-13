from rest_framework import serializers
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comments, Replies
from authors.apps.authentication.models import User
from authors.apps.profiles.models import UserProfile
from authors.apps.profiles.serializers import GetUserProfileSerializer


class RepliesSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        formats serializer display response
        :param instance:
        """
        response = super().to_representation(instance)
        profile = UserProfile.objects.get(user=instance.author)

        response['author'] = profile.user.username
        return response

    class Meta:
        model = Replies
        fields = ('id', 'reply_message', 'created_at', 'comment', 'author')


class CommentSerializer(serializers.ModelSerializer):

    replies = RepliesSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """
        formats serializer display response
        :param instance:
        """
        response = super().to_representation(instance)
        profile = UserProfile.objects.get(user=instance.author)

        response['article'] = instance.article.slug
        response['author'] = profile.user.username
        return response

    class Meta:
        model = Comments
        fields = (
            'id',
            'comment_body',
            'article',
            'author',
            'created_at',
            'replies')
