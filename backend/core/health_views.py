from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import metrics


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from django.db import connection

        db_ok = True
        try:
            connection.ensure_connection()
        except Exception:
            db_ok = False
        version = settings.SPECTACULAR_SETTINGS.get("VERSION", "unknown")
        status = "ok" if db_ok else "degraded"
        return Response({
            "status": status,
            "db": db_ok,
            "version": version,
            "service": "arca-gis-backend",
        }, status=200 if db_ok else 503)


class MetricsView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        body = metrics.render_metrics()
        return HttpResponse(body, content_type="text/plain; version=0.0.4; charset=utf-8")
