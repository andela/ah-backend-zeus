from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from authors.apps.social_auth_login.register import UserJSONRenderer
from authors.apps.social_auth_login.serializers import FacebookSocialAuthViewSerializer, GoogleSocialAuthViewSerializer, TwitterAuthViewSerializer


class FacebookSocialAuthView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer_class = FacebookSocialAuthViewSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer_class = GoogleSocialAuthViewSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TwitterSocialAuthView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer_class = TwitterAuthViewSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
