from rest_framework import serializers
from authors.apps.profiles.serializers import GetUserProfileSerializer
from .models import Article, Rating


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

    class Meta:
        model = Article
        fields = (
            'author', 'body', 'createdAt', 'description',
            'slug', 'title', 'updatedAt', 'score'
        )

    def create(self, validated_data):
        author = self.context.get('author', None)
        return Article.objects.create(author=author, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'article_id', 'score')
