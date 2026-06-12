from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin

from .s3_backup_service import backup_to_s3


class BackupTriggerView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        return Response(backup_to_s3())
