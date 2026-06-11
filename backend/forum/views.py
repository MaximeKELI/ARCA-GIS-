from rest_framework import generics, permissions

from .models import ForumCategory, ForumComment, ForumPost
from .serializers import ForumCategorySerializer, ForumCommentSerializer, ForumPostSerializer


class CategoryListView(generics.ListAPIView):
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category"]
    search_fields = ["title", "content"]

    def get_queryset(self):
        return ForumPost.objects.all()


class PostDetailView(generics.RetrieveAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = ForumCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ForumComment.objects.filter(post_id=self.kwargs["post_id"])

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs["post_id"])
