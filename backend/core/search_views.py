from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from cooperatives.models import Cooperative
from farm_ops.models import FarmTask, HarvestJournal
from forum.models import ForumPost
from parcels.models import Parcel
from training.models import Course


class GlobalSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if len(q) < 2:
            return Response({"results": [], "count": 0})

        user = request.user
        results = []

        for p in Parcel.objects.filter(owner=user, is_active=True).filter(name__icontains=q)[:5]:
            results.append({
                "type": "parcel", "id": p.id, "title": p.name,
                "subtitle": f"{p.crop_type} · {p.area_hectares or 0} ha",
            })

        for t in FarmTask.objects.filter(owner=user, title__icontains=q)[:5]:
            results.append({
                "type": "task", "id": t.id, "title": t.title,
                "subtitle": f"Échéance {t.due_date} · {t.status}",
            })

        for h in HarvestJournal.objects.filter(owner=user, crop_type__icontains=q)[:5]:
            results.append({
                "type": "harvest", "id": h.id,
                "title": f"{h.quantity_kg} kg {h.crop_type}",
                "subtitle": str(h.harvest_date),
            })

        for c in Cooperative.objects.filter(members=user, name__icontains=q)[:5]:
            results.append({
                "type": "cooperative", "id": c.id, "title": c.name,
                "subtitle": f"{c.region} · {c.member_count} membres",
            })

        for course in Course.objects.filter(is_published=True, title__icontains=q)[:5]:
            results.append({
                "type": "course", "id": course.id, "title": course.title,
                "subtitle": f"{course.duration_minutes} min · {course.category}",
            })

        for post in ForumPost.objects.filter(title__icontains=q)[:5]:
            results.append({
                "type": "forum", "id": post.id, "title": post.title,
                "subtitle": post.author.get_full_name(),
            })

        return Response({"results": results, "count": len(results)})
