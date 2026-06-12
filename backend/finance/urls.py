from django.urls import path

from .views import GenerateInvoiceView, InvoiceListView, MicroLoanListCreateView

urlpatterns = [
    path("loans/", MicroLoanListCreateView.as_view()),
    path("invoices/", InvoiceListView.as_view()),
    path("invoices/generate/", GenerateInvoiceView.as_view()),
]
