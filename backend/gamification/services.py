from .models import Badge, PointEvent, UserProfile

POINT_ACTIONS = {
    "login": 1,
    "parcel_created": 20,
    "sos_resolved": 50,
    "course_completed": 30,
    "forum_post": 10,
    "harvest_recorded": 25,
    "ai_analysis": 5,
}


def award_points(user, action: str) -> dict:
    pts = POINT_ACTIONS.get(action, 0)
    if pts == 0:
        return {"points": 0}

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.add_points(pts)
    PointEvent.objects.create(user=user, action=action, points=pts)

    new_badges = []
    for badge in Badge.objects.all():
        if badge not in profile.badges.all():
            if _check_criteria(profile, badge):
                profile.badges.add(badge)
                profile.add_points(badge.points)
                new_badges.append(badge.name)

    return {
        "points_awarded": pts,
        "total_points": profile.total_points,
        "level": profile.level,
        "new_badges": new_badges,
    }


def _check_criteria(profile, badge) -> bool:
    criteria = badge.criteria
    if "min_points" in criteria and profile.total_points >= criteria["min_points"]:
        return True
    if "min_parcels" in criteria:
        from parcels.models import Parcel
        if Parcel.objects.filter(owner=profile.user).count() >= criteria["min_parcels"]:
            return True
    return False


def get_leaderboard(limit: int = 20):
    return UserProfile.objects.order_by("-total_points")[:limit]
