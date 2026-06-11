from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LeaderboardSerializer, UserProfileSerializer
from .services import award_points, get_leaderboard


class MyGamificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from .models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)


class AwardPointsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        if not action:
            return Response({"error": "action requis"}, status=400)
        return Response(award_points(request.user, action))


class LeaderboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profiles = get_leaderboard()
        return Response(LeaderboardSerializer(profiles, many=True).data)
