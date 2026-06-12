from django.urls import path

from .poll_views import PollListCreateView, PollVoteView
from .views import CategoryListView, CommentListCreateView, PostDetailView, PostListCreateView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("posts/", PostListCreateView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:post_id>/comments/", CommentListCreateView.as_view()),
    path("polls/", PollListCreateView.as_view()),
    path("polls/<int:pk>/vote/", PollVoteView.as_view()),
]
