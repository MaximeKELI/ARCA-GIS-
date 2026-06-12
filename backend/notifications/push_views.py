from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .fcm_service import send_push
from .models import DeviceToken, PushNotification


class SendPushView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get("title", "ARCA-GIS")
        body = request.data.get("body", "")
        token = DeviceToken.objects.filter(user=request.user).first()
        if not token:
            return Response({"error": "Aucun appareil enregistré"}, status=400)
        result = send_push(token.token, title, body, request.data.get("data"))
        PushNotification.objects.create(user=request.user, title=title, body=body, data=request.data.get("data", {}))
        return Response(result)
