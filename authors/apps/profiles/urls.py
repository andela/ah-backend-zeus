from django.urls import path

from .views import UserProfiles, Updateprofile, FollowsView, FollowersView, FavoriteArticle

urlpatterns = [
    path('users/profiles', UserProfiles.as_view()),
    path('users/profiles/', Updateprofile.as_view(),name="profile"),
    path('users/article/favorite/<slug>',FavoriteArticle.as_view()),
    path('profiles/<username>/follows/', FollowsView.as_view()),
    path('profiles/<username>/followers/', FollowersView.as_view()),
]
