import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_whatsapp(phone: str, message: str) -> dict:
    """WhatsApp Business API via Twilio ou Meta Cloud API."""
    sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
    token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
    from_wa = getattr(settings, "TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

    if sid and token:
        try:
            resp = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
                auth=(sid, token),
                data={"To": f"whatsapp:{phone}", "From": from_wa, "Body": message},
                timeout=10,
            )
            return {"status": "sent" if resp.status_code == 201 else "failed", "provider": "twilio_whatsapp"}
        except requests.RequestException as e:
            logger.warning("WhatsApp failed: %s", e)

    return {"status": "queued", "note": "Configurer Twilio WhatsApp ou Meta Cloud API"}
