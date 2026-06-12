from django.conf import settings
from django.db import models


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    resource_type = models.CharField(max_length=50)
    resource_id = models.PositiveIntegerField()
    label = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "resource_type", "resource_id"]
        ordering = ["-created_at"]
