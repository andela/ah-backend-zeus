from rest_framework import serializers
from .models import UserProfile


class GetUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['photo','bio','fun_fact']
