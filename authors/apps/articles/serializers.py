from rest_framework import serializers
from authors.apps.profiles.serializers import GetUserProfileSerializer
from .models import (
    Article, Rating, Impressions, Report, Tag
)
from .relations import TagRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes article requests and creates a new article.
    """
    author = GetUserProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
    score = serializers.FloatField(required=False)
    tagList = TagRelatedField(many=True, required=False, source='tags')

    class Meta:
        model = Article
        fields = (
            'author', 'body', 'createdAt', 'description',
            'slug', 'title', 'updatedAt', 'score', 'images',
            'likes', 'dislikes', 'tagList'
        )

    def create(self, validated_data):
        author = self.context.get('author', None)
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(author=author, **validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'article_id', 'score')


class ImpressionSerializer(serializers.ModelSerializer):
    """
    Serializes impressions requests and adds to an Article.
    """

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Impressions
        fields = (
            'slug',
            'user',
            'likes',
            'dislikes',
            'updatedAt',
            'createdAt',
        )

    def get_created_at(self, instance):

        return instance.created_at.isoformat()

    def get_updated_at(self, instance):

        return instance.updated_at.isoformat()


class ArticleReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, obj):
        return obj.tag
