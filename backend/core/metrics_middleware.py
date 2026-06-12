from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from . import metrics


class MetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith("/metrics"):
            metrics.inc_requests()

    def process_response(self, request, response):
        if response.status_code >= 500:
            metrics.inc_errors()
        return response
