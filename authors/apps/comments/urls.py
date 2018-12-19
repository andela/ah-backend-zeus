"""
Defines urls used in comments package
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from authors.apps.comments.views import CommentsView, RepliesView, LikeComment

urlpatterns = [

    path('<slug>/comments/', CommentsView.as_view()),
    path('comment/<Id>/', CommentsView.as_view()),
    path('comment/<commentID>/replies/', RepliesView.as_view()),
    path('comment/replies/<Id>/', RepliesView.as_view()),
    path('comment/like/<comment_id>', LikeComment.as_view()),

]

router = DefaultRouter()

urlpatterns += router.urls
