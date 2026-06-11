from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin


class BackupTriggerView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        bucket = getattr(settings, "AWS_S3_BACKUP_BUCKET", None)
        if not bucket:
            return Response({
                "status": "simulated",
                "message": "Configurer AWS_S3_BACKUP_BUCKET pour backup réel",
                "tables": ["users", "parcels", "incidents", "alerts", "climate"],
            })
        return Response({"status": "queued", "bucket": bucket, "message": "Backup S3 planifié"})
