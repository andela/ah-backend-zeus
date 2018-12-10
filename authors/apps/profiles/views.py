from django.shortcuts import render
from .serializers import GetUserProfileSerializer, UpdateProfileSerializer
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .models import UserProfile


class UserProfiles(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = GetUserProfileSerializer


class Updateprofile(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UpdateProfileSerializer

    def update(self,request):
        serializer =self.serializer_class(request.user.userprofile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.userprofile, request.data)
        return Response(serializer.data)