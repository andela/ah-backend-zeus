from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from authors.apps.comments.models import Comments, Replies
from authors.apps.articles.models import Article
from authors.apps.comments.serializers import RepliesSerializer, CommentSerializer


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
