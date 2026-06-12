from django.conf import settings
from django.db import models


class ForumPoll(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    options = models.JSONField(default=list)
    votes = models.JSONField(default=dict)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
