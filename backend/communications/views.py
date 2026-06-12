from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin

from .services import broadcast_radio, generate_voice_message, handle_ussd, initiate_voice_call, send_sms
from .whatsapp_service import send_whatsapp


class SendSMSView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get("phone")
        message = request.data.get("message")
        if not phone or not message:
            return Response({"error": "phone et message requis"}, status=400)
        result = send_sms(phone, message, request.data.get("type", "alert"))
        return Response(result)


class USSDWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        session_id = request.data.get("sessionId", "")
        phone = request.data.get("phoneNumber", "")
        text = request.data.get("text", "")
        response_text = handle_ussd(session_id, phone, text)
        return Response(response_text, content_type="text/plain")


class VoiceMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get("text", "")
        language = request.data.get("language", request.user.preferred_language if hasattr(request.user, "preferred_language") else "fr")
        return Response(generate_voice_message(text, language))


class VoiceCallView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get("phone", request.user.phone)
        message = request.data.get("message", "Urgence ARCA-GIS. Secours en route.")
        if not phone:
            return Response({"error": "Numéro requis"}, status=400)
        return Response(initiate_voice_call(phone, message))


class WhatsAppSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get("phone", request.user.phone)
        message = request.data.get("message", "")
        if not phone or not message:
            return Response({"error": "phone et message requis"}, status=400)
        return Response(send_whatsapp(phone, message))


class RadioBroadcastView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        result = broadcast_radio(
            request.data.get("station_name", "Radio Communautaire"),
            request.data.get("region", ""),
            request.data.get("message", ""),
            request.data.get("alert_type", "climate"),
        )
        return Response(result, status=201)
