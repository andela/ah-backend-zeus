from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import (
    GetUserProfileSerializer, UpdateProfileSerializer, FavoriteArticleSerializer, FollowSerializer
)
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from .models import UserProfile, Follow
from authors.apps.authentication.models import User
from rest_framework.exceptions import NotFound
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
        

class FollowsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username):
        follower_id = User.objects.get(username=request.user.username).id
        try:
            followed_id = User.objects.get(username=username).id
            self.profile_id = UserProfile.objects.get(user_id=followed_id).id
            self.verify_following_criteria_met(follower_id, followed_id, username)
        except Exception as e:
            if isinstance(e, User.DoesNotExist):
                raise NotFound('No user with name {} exists.'.format(username))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        follow_data = {'follower': follower_id, 'followed': self.profile_id}
        serializer = FollowSerializer(data=follow_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        profile = self.get_followed_profile(self.profile_id)
        return Response(profile, status=status.HTTP_201_CREATED)
    
    def verify_following_criteria_met(self, follower_id, followed_id, name):
        if follower_id == followed_id:
            raise Exception('You cannot follow your own profile.')
        query_result = Follow.objects.filter(follower_id=follower_id, followed_id=self.profile_id)
        if len(query_result) != 0:
            raise Exception('Already following {}.'.format(name))
    
    def get_followed_profile(self, followed):
        profile = UserProfile.objects.get(id=followed)
        serializer = GetUserProfileSerializer(profile)
        profile = serializer.data
        profile['following'] = True
        return profile
    
    def delete(self, request, username):
        user_id = User.objects.get(username=request.user.username).id
        try:
            followed_id = User.objects.get(username=username).id
            profile_id = UserProfile.objects.get(user_id=followed_id).id
            follow = Follow.objects.filter(follower_id=user_id, followed_id=profile_id)
            if len(follow) == 0:
                raise Exception('Cannot unfollow a user you are not following.')
            follow.delete()
            return Response(
                {'message': 'Successfully unfollowed {}.'.format(username)},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            if isinstance(e, User.DoesNotExist):
                return Response(
                    {'error': 'No user with name {} exists.'.format(username)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request, username):
        try:
            user_id = User.objects.get(username=username).id
        except:
            raise NotFound('No user with name {} exists.'.format(username))
        follows = Follow.objects.filter(follower_id=user_id)
        serializer = FollowSerializer(follows, many=True)
        following = list()
        for follow in serializer.data:
            user_id = UserProfile.objects.get(id=follow['followed']).user_id
            username = User.objects.get(id=user_id).username
            following.append(username)
        return Response({'following': following}, status=status.HTTP_200_OK)


class FollowersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        try:
            user_id = User.objects.get(username=username).id
        except:
            raise NotFound('No user with name {} exists.'.format(username))
        profile_id = UserProfile.objects.get(user_id=user_id).id
        followers = Follow.objects.filter(followed_id=profile_id)
        serializer = FollowSerializer(followers, many=True)
        followers = list()
        for follow in serializer.data:
            username = User.objects.get(id=follow['follower']).username
            followers.append(username)
        return Response({'followers': followers}, status=status.HTTP_200_OK)
