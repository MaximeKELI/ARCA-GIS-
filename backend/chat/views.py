from rest_framework import generics, permissions

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        incident_id = self.kwargs["incident_id"]
        return ChatMessage.objects.filter(incident_id=incident_id)

    def perform_create(self, serializer):
        serializer.save(incident_id=self.kwargs["incident_id"])
