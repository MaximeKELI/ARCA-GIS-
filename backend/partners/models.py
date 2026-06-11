import secrets

from django.db import models


class PartnerAPIKey(models.Model):
    class PartnerType(models.TextChoices):
        FAO = "fao", "FAO"
        NGO = "ngo", "ONG"
        GOVERNMENT = "government", "Gouvernement"
        RESEARCH = "research", "Recherche"
        PRIVATE = "private", "Privé"

    name = models.CharField(max_length=200)
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices)
    api_key = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    rate_limit = models.PositiveIntegerField(default=1000)
    allowed_endpoints = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = f"arca_{secrets.token_hex(24)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
