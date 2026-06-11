import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def send_push_notification(user, title: str, body: str, data: dict | None = None):
    """Envoie une notification push via FCM si configuré."""
    from .models import DeviceToken, PushNotification

    PushNotification.objects.create(
        user=user, title=title, body=body, data=data or {}, sent=False
    )

    tokens = DeviceToken.objects.filter(user=user, is_active=True)
    if not tokens.exists():
        return False

    fcm_key = getattr(settings, "FCM_SERVER_KEY", None)
    if not fcm_key:
        logger.info("FCM non configuré — notification stockée pour %s", user.username)
        return False

    try:
        import requests
        for device in tokens:
            requests.post(
                "https://fcm.googleapis.com/fcm/send",
                headers={
                    "Authorization": f"key={fcm_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "to": device.token,
                    "notification": {"title": title, "body": body},
                    "data": data or {},
                },
                timeout=5,
            )
        PushNotification.objects.filter(user=user, title=title, sent=False).update(sent=True)
        return True
    except Exception as e:
        logger.warning("FCM error: %s", e)
        return False


def send_push_to_role(role: str, title: str, body: str, data: dict | None = None):
    from users.models import User

    users = User.objects.filter(role=role, is_available=True)
    for user in users:
        send_push_notification(user, title, body, data)
