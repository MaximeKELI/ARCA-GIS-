from rest_framework import serializers

from .models import ForumCategory, ForumComment, ForumPost


class ForumCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumCategory
        fields = ["id", "name", "slug", "region", "description", "post_count"]

    def get_post_count(self, obj):
        return obj.posts.count()


class ForumCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)

    class Meta:
        model = ForumComment
        fields = ["id", "post", "author", "author_name", "content", "created_at"]
        read_only_fields = ["id", "author", "created_at"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    comment_count = serializers.SerializerMethodField()
    comments = ForumCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ForumPost
        fields = [
            "id", "author", "author_name", "category", "title", "content",
            "likes", "is_pinned", "comment_count", "comments", "created_at",
        ]
        read_only_fields = ["id", "author", "likes", "created_at"]

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
