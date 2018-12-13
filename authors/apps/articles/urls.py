from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ArticleRetrieve, RatingsView


urlpatterns = [
    path('articles/', ArticleViewSet.as_view()),
    path('articles/<slug>', ArticleRetrieve.as_view()),
    path('articles/<slug>/ratings/', RatingsView.as_view()),
]
