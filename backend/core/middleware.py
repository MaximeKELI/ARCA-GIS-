import time

from django.core.cache import cache
from django.http import JsonResponse

from .models import AuditLog


class RateLimitMiddleware:
    """Limite les requêtes API: 120/min par IP, 300/min authentifié."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            key = f"rl:{request.META.get('REMOTE_ADDR', 'unknown')}"
            if hasattr(request, "user") and request.user.is_authenticated:
                key = f"rl:user:{request.user.id}"
                limit = 300
            else:
                limit = 120

            count = cache.get(key, 0)
            if count >= limit:
                return JsonResponse({"error": "Trop de requêtes. Réessayez plus tard."}, status=429)
            cache.set(key, count + 1, 60)

        return self.get_response(request)


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/") and request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if response.status_code < 400:
                user = getattr(request, "user", None)
                AuditLog.objects.create(
                    user=user if user and user.is_authenticated else None,
                    action=f"{request.method} {request.path}",
                    ip_address=request.META.get("REMOTE_ADDR"),
                    details={"status": response.status_code},
                )
        return response
