from rest_framework import serializers

from .models import Invoice, MicroLoan


class MicroLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroLoan
        fields = [
            "id", "borrower", "amount", "currency", "interest_rate",
            "crop_type", "purpose", "status", "due_date", "created_at",
        ]
        read_only_fields = ["id", "borrower", "created_at"]

    def create(self, validated_data):
        validated_data["borrower"] = self.context["request"].user
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "reference", "description", "amount", "currency", "pdf_path", "paid", "created_at"]
        read_only_fields = ["id", "reference", "pdf_path", "created_at"]
