from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_certificate_pdf(user, course, certificate_id: str) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "ARCA-GIS — Certificat de formation")
    c.setFont("Helvetica", 14)
    c.drawString(50, 700, f"Décerné à: {user.get_full_name()}")
    c.drawString(50, 670, f"Cours: {course.title}")
    c.drawString(50, 640, f"Certificat N°: {certificate_id}")
    c.drawString(50, 610, "Plateforme ARCA-GIS — Agriculture durable en Afrique")
    c.save()
    return buf.getvalue()
