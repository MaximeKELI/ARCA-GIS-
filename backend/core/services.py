import io
from datetime import datetime

from django.template.loader import render_to_string
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_parcel_report(parcel, analysis: dict | None = None) -> bytes:
    """Génère un rapport PDF pour une parcelle."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ARCA-GIS — Rapport Parcelle", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>{parcel.name}</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Culture: {parcel.get_crop_type_display()}", styles["Normal"]))
    elements.append(Paragraph(f"Surface: {parcel.area_hectares} ha", styles["Normal"]))
    elements.append(Paragraph(f"Santé: {parcel.get_health_status_display()}", styles["Normal"]))
    elements.append(Paragraph(f"Humidité sol: {parcel.soil_moisture}%", styles["Normal"]))
    elements.append(Spacer(1, 12))

    if analysis:
        elements.append(Paragraph("Analyse IA", styles["Heading3"]))
        weather = analysis.get("weather", {})
        data = [
            ["Température", f"{weather.get('temperature', 'N/A')}°C"],
            ["Pluie", f"{weather.get('rainfall_mm', 'N/A')} mm"],
            ["Humidité", f"{weather.get('humidity', 'N/A')}%"],
            ["Santé culture", analysis.get("crop_health", "N/A")],
        ]
        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        for rec in analysis.get("recommendations", []):
            elements.append(Paragraph(f"• {rec}", styles["Normal"]))

    elements.append(Spacer(1, 24))
    elements.append(Paragraph(
        f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')} — ARCA-GIS Africa",
        styles["Normal"],
    ))
    doc.build(elements)
    return buffer.getvalue()


def check_geofence(lat: float, lng: float, user) -> list[dict]:
    """Vérifie si un point est dans des zones géofencées actives."""
    from django.contrib.gis.geos import Point

    from .models import GeofenceZone

    point = Point(lng, lat, srid=4326)
    zones = GeofenceZone.objects.filter(is_active=True, geometry__contains=point)
    results = []
    for zone in zones:
        results.append({
            "zone_id": zone.id,
            "name": zone.name,
            "zone_type": zone.zone_type,
            "alert_on_enter": zone.alert_on_enter,
            "description": zone.description,
        })
    return results
