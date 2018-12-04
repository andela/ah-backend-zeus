from django.shortcuts import render
from .serializers import GetUserProfileSerializer, UpdateProfileSerializer
from rest_framework import generics, viewsets
from .models import UserProfile


class UserProfiles(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = GetUserProfileSerializer

class Updateprofile(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateProfileSerializer
    lookup_field = 'user_id'
