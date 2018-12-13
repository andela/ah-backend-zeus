from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,
    ListCreateAPIView)
from .models import Article
from authors.apps.profiles.models import UserProfile
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,
    ListCreateAPIView)
from rest_framework.views import APIView
from .models import Article, Rating

from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer, RatingSerializer
from .pagination import PageNumbering
from django.db.models import Avg
from authors.apps.authentication.models import User
from authors.apps.profiles.models import UserProfile


class ArticleViewSet(ListCreateAPIView):
    """
    article creation view
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    pagination_class = PageNumbering

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    pagination_class = PageNumbering

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

        return Response(
            "The Article has been successfully deleted",
            status=status.HTTP_204_NO_CONTENT)


class RatingsView(APIView):
    """
    View to add ratings to articles.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            user = User.objects.get(username=request.user.username)
            profile = UserProfile.objects.get(user_id=user.id)
            rating = {
                'user': profile.id,
                'article_id': article.id,
                'score': request.data['rating']
            }
            assert 1 <= request.data['rating'] <= 5, (
                'Rating should be from 1 to 5'
            )
        except Exception as e:
            if isinstance(e, AssertionError) or isinstance(e, KeyError):
                message = {'error': str(e)}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            raise NotFound(str(e))
        self.store_rating(rating)
        self.update_article_rating(article.id)
        return Response({'message': 'Rating successfully updated.'}, status=201)
    
    def store_rating(self, rating):
        try:
            article_rating = Rating.objects.filter(
                article_id=rating['article_id'],
                user=rating['user']
            )[0]
            article_rating.score = rating['score']
            article_rating.save()
        except:
            serializer = RatingSerializer(data=rating)
            serializer.is_valid(raise_exception=True)
            serializer.save()
    
    def update_article_rating(self, article_id):
        article_ratings = Rating.objects.all().filter(article_id=article_id)
        average = article_ratings.aggregate(Avg('score'))
        article = Article.objects.filter(id=article_id)[0]
        article.score = round(average['score__avg'], 1)
        article.save()
