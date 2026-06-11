from django.db import models


class SMSLog(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=[
        ("sos", "SOS"), ("alert", "Alerte"), ("voice", "Vocal"), ("ussd", "USSD"),
    ])
    status = models.CharField(max_length=20, default="pending")
    provider = models.CharField(max_length=50, default="africas_talking")
    provider_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RadioBroadcast(models.Model):
    station_name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100)
    message = models.TextField()
    alert_type = models.CharField(max_length=50)
    is_broadcast = models.BooleanField(default=False)
    broadcast_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
