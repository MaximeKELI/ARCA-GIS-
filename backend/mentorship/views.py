from rest_framework import generics, permissions

from .models import Mentorship, MentorshipSession
from .serializers import MentorshipSerializer, MentorshipSessionSerializer


class MentorshipListCreateView(generics.ListCreateAPIView):
    serializer_class = MentorshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Mentorship.objects.filter(mentor=user) | Mentorship.objects.filter(mentee=user)


class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = MentorshipSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MentorshipSession.objects.filter(mentorship_id=self.kwargs["mentorship_id"])

    def perform_create(self, serializer):
        serializer.save(mentorship_id=self.kwargs["mentorship_id"])
