from rest_framework import serializers
from .models import UserProfile, Follow


class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['photo','bio','fun_fact']


class FavoriteArticleSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ['favorite_article']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'followed')
