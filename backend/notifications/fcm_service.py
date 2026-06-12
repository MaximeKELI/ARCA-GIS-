import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_push(token: str, title: str, body: str, data: dict | None = None) -> dict:
    """Envoi notification FCM (legacy HTTP API)."""
    server_key = getattr(settings, "FCM_SERVER_KEY", None)
    if not server_key:
        return {"status": "simulated", "title": title, "body": body}

    try:
        resp = requests.post(
            "https://fcm.googleapis.com/fcm/send",
            headers={"Authorization": f"key={server_key}", "Content-Type": "application/json"},
            data=json.dumps({
                "to": token,
                "notification": {"title": title, "body": body, "sound": "default"},
                "data": data or {},
            }),
            timeout=10,
        )
        return {"status": "sent" if resp.status_code == 200 else "failed", "response": resp.json()}
    except requests.RequestException as e:
        logger.warning("FCM error: %s", e)
        return {"status": "failed", "error": str(e)}
