from rest_framework import authentication, exceptions

from .models import PartnerAPIKey


class PartnerAPIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get("X-ARCA-API-Key") or request.query_params.get("api_key")
        if not key:
            return None
        try:
            partner = PartnerAPIKey.objects.get(api_key=key, is_active=True)
        except PartnerAPIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed("Clé API partenaire invalide")
        return (None, partner)
