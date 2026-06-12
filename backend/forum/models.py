from django.conf import settings
from django.db import models


class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "forum categories"

    def __str__(self):
        return self.name


class ForumPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_posts")
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=300)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]


class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


from .poll_models import ForumPoll  # noqa: E402, F401
