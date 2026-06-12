import uuid

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice, MicroLoan
from .serializers import InvoiceSerializer, MicroLoanSerializer


class MicroLoanListCreateView(generics.ListCreateAPIView):
    serializer_class = MicroLoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MicroLoan.objects.filter(borrower=self.request.user)


class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class GenerateInvoiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ref = f"INV-{uuid.uuid4().hex[:8].upper()}"
        invoice = Invoice.objects.create(
            user=request.user,
            reference=ref,
            description=request.data.get("description", "Abonnement ARCA-GIS"),
            amount=request.data.get("amount", 5000),
        )
        try:
            from core.invoice_service import generate_invoice_pdf
            invoice.pdf_path = generate_invoice_pdf(invoice)
            invoice.save()
        except Exception:
            pass
        return Response(InvoiceSerializer(invoice).data, status=201)
