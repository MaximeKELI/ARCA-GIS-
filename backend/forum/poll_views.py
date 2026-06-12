from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .poll_models import ForumPoll


class PollListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response([{
            "id": p.id, "question": p.question, "options": p.options, "votes": p.votes,
        } for p in ForumPoll.objects.all()[:20]])

    def post(self, request):
        p = ForumPoll.objects.create(
            author=request.user, question=request.data.get("question"),
            options=request.data.get("options", []),
        )
        return Response({"id": p.id}, status=201)


class PollVoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            poll = ForumPoll.objects.get(pk=pk)
        except ForumPoll.DoesNotExist:
            return Response({"error": "Sondage introuvable"}, status=404)
        choice = request.data.get("choice")
        votes = poll.votes or {}
        votes[choice] = votes.get(choice, 0) + 1
        poll.votes = votes
        poll.save()
        return Response({"votes": poll.votes})
