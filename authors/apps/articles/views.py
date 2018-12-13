from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView)
from .models import (
    Article, Impressions)
from .renderers import ArticleJSONRenderer
from .serializers import (
    ArticleSerializer, ImpressionSerializer)
from ..authentication.models import User
from django.db.models import Count


class ArticleViewSet(ListCreateAPIView):
    """
    article creation view
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def create(self, request):
        serializer_context = {'author': request.user.userprofile}
        serializer_data = request.data.get('article', {})
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class ArticleRetrieve(RetrieveUpdateDestroyAPIView):
    """
    article retrieve, update and delete views
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(serializer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})
        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        self.perform_destroy(serializer_instance)
        return Response(
            "Article successfully deleted!",
            status=status.HTTP_204_NO_CONTENT)


class LikeArticle(ListCreateAPIView):
    """
    article like view
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        user = User.objects.get(username=request.user.username)

        impression = {
            'user': user.id,
            'likes': True,
            'dislikes': False,
            'slug': slug
        }
        self.updateimpression(impression)
        try:
            impression = Impressions.objects.all().filter(slug=slug, likes=True)
            total_likes = impression.aggregate(Count('likes'))
            article = Article.objects.get(slug=slug)
            article.likes = total_likes['likes__count']
            article.save()
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        return Response(
            {'i like this article'},
            status=status.HTTP_201_CREATED)

    def updateimpression(self, impression):
        try:
            item = Impressions.objects.filter(
                user = impression['user'],
                slug = impression['slug']
            )[0]
            if item.likes == True:
                item.likes = False
            elif item.likes == False and item.dislikes == True:
                item.likes = True
                item.dislikes = False
            item.save()
        except:
            serializer = ImpressionSerializer(
                data=impression
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()


class DislikeArticle(ListCreateAPIView):
    """
    article dislike view
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        user = User.objects.get(username=request.user.username)

        impression = {
            'user': user.id,
            'likes': False,
            'dislikes': True,
            'slug': slug
        }

        self.updateimpression(impression)
        try:
            impression = Impressions.objects.all().filter(slug=slug, dislikes=True)
            total_dislikes = impression.aggregate(Count('dislikes'))
            article = Article.objects.get(slug=slug)
            article.dislikes = total_dislikes['dislikes__count']
            article.save()
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        return Response(
            {'i dislike this article'},
            status=status.HTTP_201_CREATED)

    def updateimpression(self, impression):
        try:
            item = Impressions.objects.filter(
                user = impression['user'],
                slug = impression['slug']
            )[0]
            if item.dislikes == True:
                item.dislikes = False
            elif item.dislikes == False and item.likes == True:
                item.dislikes = True
                item.likes = False
            item.save()
        except:
            serializer = ImpressionSerializer(
                data=impression
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

