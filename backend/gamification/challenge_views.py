from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .challenge_models import SeasonalChallenge


class ChallengeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        region = request.query_params.get("region", request.user.region)
        qs = SeasonalChallenge.objects.filter(is_active=True)
        if region:
            qs = qs.filter(region=region) | qs.filter(region="")
        return Response([{
            "id": c.id, "title": c.title, "description": c.description,
            "points": c.points_reward, "target": c.target_count,
        } for c in qs.distinct()])


class RegionalLeaderboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        region = request.query_params.get("region")
        from .models import UserProfile
        qs = UserProfile.objects.select_related("user")
        if region:
            qs = qs.filter(user__region=region)
        qs = qs.order_by("-total_points")[:20]
        return Response([{
            "username": p.user.username, "points": p.total_points,
            "region": p.user.region, "level": p.level,
        } for p in qs])
