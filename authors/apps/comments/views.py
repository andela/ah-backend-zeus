from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from authors.apps.comments.models import Comments, Replies, Impressions
from authors.apps.articles.models import Article
from authors.apps.comments.serializers import RepliesSerializer, CommentSerializer, ImpressionSerializer
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,
    ListCreateAPIView)
from ..authentication.models import User
from django.db.models import Count


def get_object(obj_Class, pk):
    try:
        return obj_Class.objects.get(pk=pk)

    except obj_Class.DoesNotExist:
        raise Http404


class CommentsView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, slug):
        """
        creating comments on an article
        """
        content_data = request.data.get('comment', None)
        try:
            instance = Article.objects.get(slug=slug)
            author = request.user
            content_data['article'] = instance.id
            content_data['author'] = author.id
            serializer = CommentSerializer(data=content_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Article.DoesNotExist:
            return Response(
                {"message": "Article your are trying to get doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, slug):
        """
        gets all the comments on a particular comment
        """
        instance = get_object_or_404(Article, slug=slug)
        article = instance.id
        comment = Comments.objects.all().filter(article_id=article)
        serializer = self.serializer_class(comment, many=True)
        return Response({"comments": serializer.data}, status.HTTP_200_OK)

    def put(self, request, Id):
        """
        updates the comments on an article
        """
        snippet = get_object(Comments, Id)
        content_data = request.data.get('comment', None)
        content_data['author'] = request.user.id
        serializer = CommentSerializer(snippet, data=content_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, instance, Id):
        """
        deletes your owen comment
        """
        try:
            instance = Comments.objects.get(id=Id,)
            if str(instance):
                instance.delete()
        except Comments.DoesNotExist:
            raise NotFoundException(
                "The Comment you are trying to delete is not found.")
        return Response({"message",
                         "your Comment  has been deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class RepliesView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, commentID):
        """
        replies to comment
        """
        try:
            content_data = request.data.get('reply', None)
            author = request.user
            instance = Comments.objects.get(id=commentID)
            content_data['author'] = author.id
            content_data['comment'] = instance.id
            serializer = RepliesSerializer(data=content_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Comments.DoesNotExist:
            return Response(
                {"message": "please the comment doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, Id, format=None):
        """
        deletes your owen comment
        """
        snippet = get_object(Replies, Id)
        snippet.delete()
        return Response(
            {
                "message": "Your reply to the comment has been  deleted Successfully."},
            status=status.HTTP_204_NO_CONTENT)

    def put(self, request, Id):
        """
        updates your owen comment
        """
        content = get_object(Replies, Id)
        serializer = RepliesSerializer(
            content, data=request.data.get('reply', None))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LikeComment(ListCreateAPIView):
    """
    ca view class to handle liking a comment
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, comment_id):
        user = User.objects.get(username=request.user.username)

        impression = {
            'user': user.id,
            'likes': True,
            'comment': comment_id
        }
        self.updateimpression(impression)
        try:
            impression = Impressions.objects.all().filter(comment=comment_id, likes=True)
            total_likes = impression.aggregate(Count('likes'))
            comment = Comments.objects.get(id=comment_id)
            comment.likes = total_likes['likes__count']
            comment.save()
        except Comments.DoesNotExist:
            raise NotFound('A comment with this id does not exist.')
        return Response(
            {'message': 'i liked this.'},
            status=status.HTTP_201_CREATED)

    def updateimpression(self, impression):
        try:
            item = Impressions.objects.filter(
                user = impression['user'],
                comment = impression['comment']
            )[0]
            if item.likes == True:
                item.likes = False
            else:
                item.likes = True
            item.save()
        except:
            serializer = ImpressionSerializer(
                data=impression
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()