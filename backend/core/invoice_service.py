from pathlib import Path

from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_invoice_pdf(invoice) -> str:
    media = Path(settings.MEDIA_ROOT) / "invoices"
    media.mkdir(parents=True, exist_ok=True)
    path = media / f"{invoice.reference}.pdf"

    c = canvas.Canvas(str(path), pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "ARCA-GIS — Facture")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Référence: {invoice.reference}")
    c.drawString(50, 750, f"Client: {invoice.user.get_full_name()}")
    c.drawString(50, 730, f"Description: {invoice.description}")
    c.drawString(50, 710, f"Montant: {invoice.amount} {invoice.currency}")
    c.drawString(50, 690, f"Date: {invoice.created_at.strftime('%d/%m/%Y')}")
    c.save()
    return f"invoices/{invoice.reference}.pdf"
