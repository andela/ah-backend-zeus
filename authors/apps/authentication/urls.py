from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, AccountVerified, 
    PasswordResetAPIView, PasswordUpdateAPIView, UsersRetrieveAPIView
)


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="registration"),
    path('users/login/', LoginAPIView.as_view(), name = "user_login"),
    path('users/verified_account/<token>/<uid>', AccountVerified.as_view(), name="verify_account"),
    path('users/password_reset/', PasswordResetAPIView.as_view()),
    path('users/password_update/<token>', PasswordUpdateAPIView.as_view()),
    path('authors/', UsersRetrieveAPIView.as_view())
]
