from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "farmer", "Agriculteur"
        RESCUE = "rescue", "Secours"
        ADMIN = "admin", "Administrateur"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.FARMER,
    )
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, default="Côte d'Ivoire")
    region = models.CharField(max_length=100, blank=True)
    last_position = gis_models.PointField(srid=4326, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_farmer(self):
        return self.role == self.Role.FARMER

    @property
    def is_rescue(self):
        return self.role == self.Role.RESCUE

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser
