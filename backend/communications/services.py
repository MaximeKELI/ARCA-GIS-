import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_sms(phone: str, message: str, message_type: str = "alert") -> dict:
    """Envoie SMS via Africa's Talking ou Twilio."""
    from .models import SMSLog

    log = SMSLog.objects.create(phone=phone, message=message, message_type=message_type)

    at_key = getattr(settings, "AFRICAS_TALKING_API_KEY", None)
    at_user = getattr(settings, "AFRICAS_TALKING_USERNAME", None)

    if at_key and at_user:
        try:
            resp = requests.post(
                "https://api.africastalking.com/version1/messaging",
                headers={"apiKey": at_key, "Content-Type": "application/x-www-form-urlencoded"},
                data={"username": at_user, "to": phone, "message": message},
                timeout=10,
            )
            log.status = "sent" if resp.status_code == 201 else "failed"
            log.provider_id = resp.text[:100]
            log.save()
            return {"status": log.status, "provider": "africas_talking"}
        except requests.RequestException as e:
            logger.warning("SMS failed: %s", e)

    twilio_sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
    twilio_token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
    twilio_from = getattr(settings, "TWILIO_PHONE_NUMBER", None)

    if twilio_sid and twilio_token and twilio_from:
        try:
            resp = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json",
                auth=(twilio_sid, twilio_token),
                data={"To": phone, "From": twilio_from, "Body": message},
                timeout=10,
            )
            log.status = "sent" if resp.status_code == 201 else "failed"
            log.provider = "twilio"
            log.save()
            return {"status": log.status, "provider": "twilio"}
        except requests.RequestException as e:
            logger.warning("Twilio failed: %s", e)

    log.status = "queued"
    log.save()
    logger.info("SMS queued (no provider): %s -> %s", phone, message[:50])
    return {"status": "queued", "provider": "local", "log_id": log.id}


def handle_ussd(session_id: str, phone: str, text: str) -> str:
    """Menu USSD ARCA-GIS."""
    parts = text.split("*") if text else []
    level = len(parts)

    if level == 0:
        return "CON Bienvenue ARCA-GIS\n1. SOS Urgence\n2. Meteo\n3. Prix marches\n4. Conseils\n0. Quitter"
    choice = parts[-1] if parts else ""

    if choice == "1":
        send_sms(phone, f"SOS ARCA-GIS signale par {phone}. Reponse urgente requise.", "sos")
        from alerts.services import broadcast_alert
        broadcast_alert("sos", "SOS USSD", f"SOS via USSD de {phone}", "critical", {"phone": phone}, "rescue")
        return "END SOS envoye! Secours alertes."
    elif choice == "2":
        return "END Meteo Bouake: 33C, humidite 42%. Risque secheresse eleve."
    elif choice == "3":
        return "END Prix: Mais 180F/kg, Riz 450F/kg, Cacao 1200F/kg"
    elif choice == "4":
        return "END Conseil: Irriguer tot le matin. Surveiller ravageurs."
    elif choice == "0":
        return "END Merci d'utiliser ARCA-GIS."
    return "END Option invalide."


def generate_voice_message(text: str, language: str = "fr") -> dict:
    """Génère message vocal (TTS) — retourne texte formaté pour synthèse."""
    prefixes = {"fr": "ARCA-GIS alerte:", "en": "ARCA-GIS alert:", "sw": "ARCA-GIS tahadhari:"}
    prefix = prefixes.get(language, prefixes["fr"])
    return {
        "text": f"{prefix} {text}",
        "language": language,
        "format": "text",
        "note": "Intégrer gTTS ou Amazon Polly en production",
    }


def initiate_voice_call(phone: str, message: str) -> dict:
    """Appel vocal SOS via Twilio."""
    from .models import SMSLog

    log = SMSLog.objects.create(phone=phone, message=message, message_type="voice")

    sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
    token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
    from_number = getattr(settings, "TWILIO_PHONE_NUMBER", None)

    if sid and token and from_number:
        try:
            twiml = f'<Response><Say language="fr-FR">{message}</Say></Response>'
            resp = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json",
                auth=(sid, token),
                data={"To": phone, "From": from_number, "Twiml": twiml},
                timeout=10,
            )
            log.status = "sent" if resp.status_code == 201 else "failed"
            log.provider = "twilio_voice"
            log.save()
            return {"status": log.status, "provider": "twilio_voice"}
        except requests.RequestException as e:
            logger.warning("Voice call failed: %s", e)

    log.status = "queued"
    log.save()
    return {"status": "queued", "note": "Configurer Twilio pour appels vocaux"}


def broadcast_radio(station_name: str, region: str, message: str, alert_type: str) -> dict:
    from django.utils import timezone
    from .models import RadioBroadcast

    broadcast = RadioBroadcast.objects.create(
        station_name=station_name,
        region=region,
        message=message,
        alert_type=alert_type,
        is_broadcast=True,
        broadcast_at=timezone.now(),
    )
    return {"id": broadcast.id, "status": "broadcast", "station": station_name}
