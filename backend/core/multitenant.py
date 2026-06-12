"""Middleware multi-tenant par pays/organisation."""

from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tenant = request.headers.get("X-ARCA-Tenant", "default")
        request.tenant_id = tenant
