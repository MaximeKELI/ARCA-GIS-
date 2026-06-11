from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .two_factor import generate_qr_base64, generate_totp_secret, get_totp_uri, verify_totp


class Setup2FAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        secret = generate_totp_secret()
        request.user.totp_secret = secret
        request.user.save(update_fields=["totp_secret"])
        uri = get_totp_uri(request.user, secret)
        return Response({
            "secret": secret,
            "qr_base64": generate_qr_base64(uri),
            "uri": uri,
        })


class Enable2FAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        if not code or not request.user.totp_secret:
            return Response({"error": "Code requis"}, status=400)
        if not verify_totp(request.user.totp_secret, code):
            return Response({"error": "Code invalide"}, status=400)
        request.user.is_2fa_enabled = True
        request.user.save(update_fields=["is_2fa_enabled"])
        return Response({"status": "2FA activé"})


class Verify2FAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        if not request.user.is_2fa_enabled:
            return Response({"valid": True, "note": "2FA non activé"})
        if verify_totp(request.user.totp_secret, code):
            return Response({"valid": True})
        return Response({"valid": False}, status=400)
