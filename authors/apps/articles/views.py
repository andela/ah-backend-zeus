from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,APIException
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    ListCreateAPIView, ListAPIView)
from .models import (
    Article, Impressions, Rating, Report, Tag)
from .renderers import ArticleJSONRenderer
from .serializers import (
    ArticleSerializer, ImpressionSerializer,
    RatingSerializer, ArticleReportSerializer, 
    TagSerializer, BookMarkArticleSerializer)
from .pagination import PageNumbering
from django.db.models import Avg
from authors.apps.articles.models import Article, BookMarkArticle
from authors.apps.profiles.models import UserProfile
from ..authentication.models import User
from django.db.models import Count
import os
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
import jwt
from authors.settings import EMAIL_HOST_USER, SECRET_KEY
from django.core.mail import send_mail


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

        self.perform_destroy(serializer_instance)
        return Response(
            "Article successfully deleted!",
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
            impression = Impressions.objects.all().filter(slug=slug, dislikes=True)
            total_dislikes = impression.aggregate(Count('dislikes'))
            article = Article.objects.get(slug=slug)
            article.likes = total_likes['likes__count']
            article.dislikes = total_dislikes['dislikes__count']
            article.save()
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        return Response(
            {'message': 'i like this article.'},
            status=status.HTTP_201_CREATED)

    def updateimpression(self, impression):
        try:
            item = Impressions.objects.filter(
                user=impression['user'],
                slug=impression['slug']
            )[0]
            if item.likes == True:
                item.likes = False
                item.dislikes = False
            else:
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
            impression = Impressions.objects.all().filter(slug=slug, likes=True)
            total_likes = impression.aggregate(Count('likes'))
            impression = Impressions.objects.all().filter(slug=slug, dislikes=True)
            total_dislikes = impression.aggregate(Count('dislikes'))
            article = Article.objects.get(slug=slug)
            article.likes = total_likes['likes__count']
            article.dislikes = total_dislikes['dislikes__count']
            article.save()
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        return Response(
            {'message': 'i dislike this article'},
            status=status.HTTP_201_CREATED)

    def updateimpression(self, impression):
        try:
            item = Impressions.objects.filter(
                user=impression['user'],
                slug=impression['slug']
            )[0]
            if item.dislikes == True:
                item.dislikes = False
                item.likes = False
            else:
                item.dislikes = True
                item.likes = False
            item.save()
        except:
            serializer = ImpressionSerializer(
                data=impression
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()


class ReportArticlesView(generics.GenericAPIView):
    """
    Report articles violating terms of agreement
    """
    serializer_class = ArticleReportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_token(self, request):
        try:
            auth_header = authentication.get_authorization_header(request).split()[
                1]
            token = jwt.decode(auth_header, SECRET_KEY, 'utf-8')
            author_id = token['id']
            return author_id
        except:
            return ("Token is invalid")

    def post(self, request, slug, **kwargs):
        try:
            article_id = (Article.objects.get(slug=slug).id)
        except:
            return Response({
                "message": "Article does not exist!"
            })

        reason = request.data.get('reason')

        author_id = (self.get_token(request))

        if Report.objects.filter(reporter=author_id).filter(article=article_id).exists():
            return Response({
                "message": "You have already reported this Article"
            })
        article_data = Article.objects.get(pk=article_id)
        new_report = {
            "article": article_id,
            "article_title": article_data.title,
            "reported": True,
            "reason": reason,
            "reporter": author_id
        }

        serializer = self.serializer_class(data=new_report)
        serializer.is_valid()
        serializer.save()

        # Send a violations report email to the Authors Haven administrator

        subject = "ARTICLES VIOLATIONS ALERT"
        user = User.objects.get(pk=author_id)
        body = f"Article: {article_id}, \nReported: {new_report['reported']},\nReported by: {user.username}, \nReason: {new_report['reason']}"
        receipient = EMAIL_HOST_USER
        email_sender = EMAIL_HOST_USER
        send_mail(subject, body, email_sender, [
                  receipient], fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def taglist(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer_data
        }, status=status.HTTP_200_OK)


class BookMarkArticleView(ListCreateAPIView):
    """
    class for bookmarking and unbookmarking an article
    """
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def post(self,request,slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            return Response('An article with this slug does not exist.',status.HTTP_404_NOT_FOUND)
        obj = BookMarkArticle.objects.filter(article=slug)

        if len(obj)==0:
            bk = {'user': request.user.id, 'article': slug}
            serializer = BookMarkArticleSerializer(data=bk)
            serializer.is_valid()
            serializer.save()
        
        if obj:
            obj.delete()
            return Response({'message':'article unbookmarked'},status.HTTP_204_NO_CONTENT)
        serializer = self.serializer_class(serializer_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookMarkView(ListCreateAPIView):
    """
    class for getting bookmarked articles
    """
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    article = []
    def get(self,request):
        obj = BookMarkArticle.objects.filter(user_id=request.user.id)
        for i in obj:
            serializer_instance = self.queryset.get(slug=i.article)
            serializer = self.serializer_class(serializer_instance)
            self.article.append(serializer.data)
        
        return Response(self.article)
 

class FacebookShareView(APIView):
    """
    sharing an article on facebook
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug, **kwargs):
        slug = slug

        try:
            Article.objects.get(slug=slug)
            current_site = 'http://{}'.format(get_current_site(request))
            route = 'api/articles'
            url = "{}/{}/{}".format(current_site, route, slug)
            base_url = "https://www.facebook.com/sharer/sharer.php?u="
            url_link = base_url + url

            return Response(
                {
                    "message": "Authors Haven",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message": "Article not found."
            },
            status=status.HTTP_404_NOT_FOUND
            )

        
class TwitterShareView(APIView):
    """
    sharing an article on twitter
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug, **kwargs):
        slug = slug

        try:
            Article.objects.get(slug=slug)
            base_url = "https://twitter.com/home?status="
            current_site = 'http://{}'.format(get_current_site(request))
            route = 'api/articles'
            url = "{}/{}/{}".format(current_site, route, slug)
            url_link = base_url + url

            return Response(
                {
                    "message": "Twitterlink",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message":"Article not found"
            },
            status=status.HTTP_404_NOT_FOUND
            )

        
class EmailShareView(APIView):
    """
    sharing an article via
    """
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, slug):
        
        slug = slug
        try:
            
            Article.objects.get(slug=slug)

            current_site = 'https://{}'.format(get_current_site(request))
            route = 'api/articles'
            url = "{}/{}/{}".format(current_site, route, slug)

            from_email = os.environ.get(
                "EMAIL_HOST_USER", "seven.zeusgeek@gmail.com")
            recipient = request.user.email
            subject = "Authors Haven"
            body = "Click here to enjoy the article {}".format(url)
            send_mail(subject, body, from_email, [recipient], fail_silently=False)

            return Response(
                {
                    "message": "Email has been successfully sent",
                    "link": url
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message":"Article not found"
                
            },
            status = status.HTTP_404_NOT_FOUND
            )
class SearchArticleView(ListAPIView):
    """
    view that searches articles
    """
    permission_classes = (AllowAny, )
    serializer_class = ArticleSerializer

    def get(self, request):
        search_params = request.query_params
        query_set = Article.objects.all()

        author = search_params.get('author', None)
        title = search_params.get('title', None)
        tag = search_params.get('tag', None)
        keywords = search_params.get('keywords', None)

        if author:
            try:
                user_id = User.objects.get(username=author).id

            except User.DoesNotExist:
                raise NotFound('Specified User does not exist.')
            profile_id = UserProfile.objects.get(user_id=user_id).id
            query_set = query_set.filter(author=profile_id)
        if title:
            query_set = query_set.filter(title__icontains=title)
        if  tag:
            query_set = Article.objects.none()
            for article in Article.objects.all():
                try:
                    if article.tags.all().get(tag=tag):
                        query_set |= Article.objects.filter(title=article.title)
                except:
                    pass
        if keywords:
            words = str(keywords).split(',')
            last_queryset = ''
            for word in words:
                last_queryset = query_set.filter(title__icontains=word)
            query_set = last_queryset

        serializer = self.serializer_class(query_set, many=True)
        res_data = serializer.data

        return Response({"search results": res_data}, status.HTTP_200_OK)
