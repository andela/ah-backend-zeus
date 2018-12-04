from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .validations import validate_registration
from django.core.mail import send_mail
from authors.settings import EMAIL_HOST_USER, SECRET_KEY
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import jwt
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from rest_framework import generics
from authors.apps.authentication.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, PasswordSerializer
)
from .models import User
from django.http import JsonResponse



class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    
    def post(self, request):
        user = request.data.get('user', {})
        validate_registration(user)

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.filter(email=user['email']).first()

        RegistrationAPIView.generate_token(user, request)
        # body = "click this link to verify your account   http://localhost:8000/api/users/verified_account/{}".format(
        #     serializer.data['token'])
        # receipient = serializer.data['email']
        # email_sender = EMAIL_HOST_USER
        # send_mail(subject, body, email_sender, [receipient], fail_silently=False)
        return Response({'message': 'User successfully Registered, check your email and click the link to verify'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def generate_token(user, request):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.username)).decode('utf-8')
        current_site = 'http://{}'.format(get_current_site(request))
        route='api/users/verified_account'
        url = "{}/{}/{}/{}".format(current_site, route, token, uid)
        subject = "Hello {}".format(user.username + ", thank you for joining Authors haven")
        body = "click this link to verify your account \n {}".format(url)
        receipient = user.email
        email_sender = EMAIL_HOST_USER
        send_mail(subject, body, email_sender, [receipient], fail_silently=False)
        
        return token, uid


class AccountVerified(GenericAPIView):

    def get(self, request, token, uid):
        username = force_text(urlsafe_base64_decode(uid))

        user = User.objects.filter(username=username).first()
        verify_token = default_token_generator.check_token(user, token)

        msg = {"message": "email verified"}
        st = status.HTTP_200_OK

        if not verify_token:
            msg["message"] = "token invalid"
            st = status.HTTP_400_BAD_REQUEST

        else:
            user.is_verified = True
            user.save()

        return Response(msg, status=st)

def generate_password_reset_token(data):
    token = jwt.encode({
        'email': data
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


class PasswordResetAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def post(self, request):
        user_data = request.data['user']['email']

        if not user_data:
            return Response({"message": "Please enter your email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_data)

            token = generate_password_reset_token(user_data)

            serializer_data = self.serializer_class(user)
            email_sender = EMAIL_HOST_USER
            receipient = [serializer_data['email'].value]
            subject = "Password Reset "
            message = "Click this link to reset your password:" + "http://{}/api/users/password_update/{}".format(
                get_current_site(request), token)
            send_mail(subject, message, email_sender,
                      receipient, fail_silently=False)
            return Response(
                {'message': 'Check your email for the password reset link', "token": token}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)



class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer
    #The URL conf should include a keyword argument corresponding to this value
    look_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get(self.look_url_kwarg)
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"message": "Please enter your password"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=decode_token['email'])
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Your password has been reset'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Cannot reset password'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRetrieveAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        response = {'authors': serializer.data}
        for author, obj in zip(response['authors'], User.objects.all()):
            author['profile'] = reverse('profile', args=[obj.id], request=request)
            del author['token']
        return JsonResponse(response, status=200, safe=False)

