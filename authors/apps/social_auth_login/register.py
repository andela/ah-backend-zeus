from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer


def register_facebook_user(user_id, email, name):
    user = User.objects.filter(facebook_id=user_id)
    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)
        User.objects.filter(email=email).update(facebook_id=user_id)
        new_user = authenticate(email=email, password="XXXXXXXX")
        return new_user.token
    else:
        User.objects.filter(facebook_id=user_id)
        registered_user = authenticate(email=email, password="XXXXXXXX")
        return registered_user.token


def register_google_user(user_id, email, name):
    user = User.objects.filter(google_id=user_id)
    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)
        User.objects.filter(email=email).update(google_id=user_id)
        new_user = authenticate(email=email, password="XXXXXXXX")
        return new_user.token
    else:
        User.objects.filter(google_id=user_id)
        registered_user = authenticate(email=email, password="XXXXXXXX")
        return registered_user.token


def register_twitter_user(user_id, email, name):
    user = User.objects.filter(twitter_id=user_id)
    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)
        User.objects.filter(email=email).update(twitter_id=user_id)
        new_user = authenticate(email=email, password="XXXXXXXX")
        return new_user.token
    else:
        User.objects.filter(twitter_id=user_id)
        registered_user = authenticate(email=email, password="XXXXXXXX")
        return registered_user.token
