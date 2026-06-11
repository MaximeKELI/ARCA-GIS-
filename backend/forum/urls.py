from django.urls import path

from .views import CategoryListView, CommentListCreateView, PostDetailView, PostListCreateView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("posts/", PostListCreateView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:post_id>/comments/", CommentListCreateView.as_view()),
]
