from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class OAuthProvidersView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "providers": [
                {"id": "google", "name": "Google", "auth_url": "/api/auth/oauth/google/"},
                {"id": "microsoft", "name": "Microsoft", "auth_url": "/api/auth/oauth/microsoft/"},
            ],
            "note": "Configurer GOOGLE_OAUTH_CLIENT_ID et MS_OAUTH_CLIENT_ID en production",
        })


class OAuthCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        provider = request.data.get("provider")
        code = request.data.get("code")
        if not provider or not code:
            return Response({"error": "provider et code requis"}, status=400)
        return Response({
            "status": "oauth_simulated",
            "provider": provider,
            "message": "Échanger le code contre un JWT via le provider OAuth configuré",
        })
