from django.urls import path

from authors.apps.social_auth_login.views import (
    FacebookSocialAuthView, GoogleSocialAuthView, TwitterSocialAuthView
)

urlpatterns = [
    path('auth/facebook/', FacebookSocialAuthView.as_view()),
    path('auth/google/', GoogleSocialAuthView.as_view()),
    path('auth/twitter/', TwitterSocialAuthView.as_view()),
]
