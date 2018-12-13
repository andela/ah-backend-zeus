from django.shortcuts import render
from .serializers import GetUserProfileSerializer, UpdateProfileSerializer, FavoriteArticleSerializer
from rest_framework.generics import (ListAPIView,RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from .models import UserProfile
from ..authentication.models import User
from ..articles.models import Article


class UserProfiles(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = GetUserProfileSerializer


class Updateprofile(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UpdateProfileSerializer

    def update(self,request):
        serializer =self.serializer_class(request.user.userprofile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.userprofile, request.data)
        return Response(serializer.data)

class FavoriteArticle(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FavoriteArticleSerializer
    queryset = Article.objects.all()

    def update(self,request,slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            return Response('An article with this slug does not exist.',status.HTTP_404_NOT_FOUND)
        
        userprofile_obj = request.user.userprofile
        
        if slug in userprofile_obj.favorite_article:
            userprofile_obj.favorite_article.remove(slug)
            userprofile_obj.save() 
            return Response("unfavorited!")
        
        userprofile_obj.favorite_article.append(slug)
        userprofile_obj.save(update_fields = ['favorite_article'])
        return Response("favorited!")
        

