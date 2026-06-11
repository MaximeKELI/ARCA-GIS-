from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, CourseProgress
from .serializers import CourseProgressSerializer, CourseSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "language"]


class CourseProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Cours introuvable"}, status=404)
        progress_pct = request.data.get("progress_pct", 100)
        progress, _ = CourseProgress.objects.update_or_create(
            user=request.user, course=course,
            defaults={
                "progress_pct": progress_pct,
                "completed": progress_pct >= 100,
                "completed_at": timezone.now() if progress_pct >= 100 else None,
            },
        )
        return Response(CourseProgressSerializer(progress).data)


class MyProgressView(generics.ListAPIView):
    serializer_class = CourseProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)
