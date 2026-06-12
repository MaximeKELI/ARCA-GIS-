from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from rest_framework import permissions
from rest_framework.views import APIView

from .stats_views import VisualStatsView


def _build_stats_pdf(data: dict, user) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("ARCA-GIS — Rapport statistiques", styles["Title"]),
        Paragraph(f"Agriculteur: {user.get_full_name()}", styles["Normal"]),
        Spacer(1, 16),
    ]

    kpi_rows = [["Indicateur", "Valeur", "Unité"]]
    for k in data.get("kpis", []):
        kpi_rows.append([k.get("label", ""), str(k.get("value", "")), k.get("unit", "")])
    t = Table(kpi_rows, colWidths=[200, 100, 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7F5")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    summary = data.get("summary", {})
    story.append(Paragraph("Résumé", styles["Heading2"]))
    for label, key in [("Superficie totale (ha)", "total_area_ha"), ("SOS actifs", "active_sos"),
                       ("Événements climat", "climate_events"), ("Stock bas", "low_stock_items")]:
        story.append(Paragraph(f"• {label}: {summary.get(key, '—')}", styles["Normal"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Répartition cultures", styles["Heading2"]))
    for item in data.get("distributions", {}).get("crop_types", []):
        story.append(Paragraph(f"• {item.get('name')}: {item.get('value')}", styles["Normal"]))

    doc.build(story)
    return buf.getvalue()


class VisualStatsPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats_view = VisualStatsView()
        stats_view.request = request
        stats_view.format_kwarg = None
        data = stats_view.get(request).data
        pdf = _build_stats_pdf(data, request.user)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="arca_gis_stats.pdf"'
        return response
