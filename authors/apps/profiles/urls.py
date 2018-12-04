from django.urls import path

from .views import UserProfiles,Updateprofile

urlpatterns = [
    path('users/profiles', UserProfiles.as_view()),
    path('users/profiles/<int:user_id>/', Updateprofile.as_view(), name='profile')
]
