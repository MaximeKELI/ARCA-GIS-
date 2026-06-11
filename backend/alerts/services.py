from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Alert


def broadcast_alert(
    alert_type: str,
    title: str,
    message: str,
    severity: str = "medium",
    data: dict | None = None,
    target_role: str = "",
):
    """Crée une alerte et la diffuse via WebSocket."""
    alert = Alert.objects.create(
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        data=data or {},
        target_role=target_role,
        is_broadcast=True,
    )

    channel_layer = get_channel_layer()
    if channel_layer:
        payload = {
            "type": "alert_message",
            "alert": {
                "id": alert.id,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "title": alert.title,
                "message": alert.message,
                "data": alert.data,
                "created_at": alert.created_at.isoformat(),
            },
        }
        async_to_sync(channel_layer.group_send)("alerts", payload)
        if target_role:
            async_to_sync(channel_layer.group_send)(f"role_{target_role}", payload)

    return alert
