from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet, ArticleRetrieve,
    LikeArticle, DislikeArticle, RatingsView, ReportArticlesView)


urlpatterns = [
    path('articles/', ArticleViewSet.as_view()),
    path('articles/<slug>', ArticleRetrieve.as_view()),
    path('articles/<slug>/ratings/', RatingsView.as_view()),
    path('articles/like/<slug>', LikeArticle.as_view()),
    path('articles/dislike/<slug>', DislikeArticle.as_view()),
    path('<slug>/report_article', ReportArticlesView.as_view())
]
