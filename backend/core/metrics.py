"""Compteurs Prometheus in-memory pour monitoring ARCA-GIS."""

_REQUESTS = 0
_ERRORS = 0


def inc_requests():
    global _REQUESTS
    _REQUESTS += 1


def inc_errors():
    global _ERRORS
    _ERRORS += 1


def render_metrics():
    from django.db import connection

    from incidents.models import Incident
    from iot.models import IoTSensor
    from parcels.models import Parcel

    db_ok = 1
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = 0

    active_sos = Incident.objects.filter(status="active", incident_type="sos").count()
    parcels = Parcel.objects.filter(is_active=True).count()
    iot_online = IoTSensor.objects.filter(is_active=True).count()

    lines = [
        "# HELP http_requests_total Total HTTP requests",
        "# TYPE http_requests_total counter",
        f"http_requests_total {_REQUESTS}",
        "# HELP http_errors_total Total HTTP 5xx responses",
        "# TYPE http_errors_total counter",
        f"http_errors_total {_ERRORS}",
        "# HELP arca_active_sos Active SOS incidents",
        "# TYPE arca_active_sos gauge",
        f"arca_active_sos {active_sos}",
        "# HELP arca_parcels_active Active parcels",
        "# TYPE arca_parcels_active gauge",
        f"arca_parcels_active {parcels}",
        "# HELP arca_iot_devices_online IoT sensors registered",
        "# TYPE arca_iot_devices_online gauge",
        f"arca_iot_devices_online {iot_online}",
        "# HELP arca_db_up Database connectivity",
        "# TYPE arca_db_up gauge",
        f"arca_db_up {db_ok}",
    ]
    return "\n".join(lines) + "\n"
