from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .bookmark_models import Bookmark


class BookmarkListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Bookmark.objects.filter(user=request.user)
        return Response([{
            "id": b.id, "resource_type": b.resource_type,
            "resource_id": b.resource_id, "label": b.label,
        } for b in qs])

    def post(self, request):
        b, created = Bookmark.objects.get_or_create(
            user=request.user,
            resource_type=request.data.get("resource_type"),
            resource_id=request.data.get("resource_id"),
            defaults={"label": request.data.get("label", "")},
        )
        return Response({"id": b.id, "created": created}, status=201 if created else 200)


class BookmarkDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        deleted, _ = Bookmark.objects.filter(pk=pk, user=request.user).delete()
        return Response({"deleted": deleted > 0})
