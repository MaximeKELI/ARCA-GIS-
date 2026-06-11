from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    incident = models.ForeignKey(
        "incidents.Incident", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages"
    )
    message = models.TextField()
    attachment = models.ImageField(upload_to="chat/", blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"
