from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer
from .services import initiate_payment, verify_payment


class PaymentInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        result = initiate_payment(
            request.user,
            request.data.get("provider", "orange_money"),
            float(request.data.get("amount", 0)),
            request.data.get("phone", request.user.phone),
            request.data.get("description", "Abonnement ARCA-GIS"),
        )
        return Response(result, status=201)


class PaymentVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference):
        return Response(verify_payment(reference))


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
