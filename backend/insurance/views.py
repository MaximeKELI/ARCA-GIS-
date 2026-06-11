from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InsuranceClaim, InsurancePolicy
from .serializers import InsuranceClaimSerializer, InsurancePolicySerializer
from .services import process_claim


class PolicyListCreateView(generics.ListCreateAPIView):
    serializer_class = InsurancePolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InsurancePolicy.objects.filter(farmer=self.request.user)


class ClaimListView(generics.ListAPIView):
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InsuranceClaim.objects.filter(policy__farmer=self.request.user)


class EvaluateClaimView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        return Response(process_claim(pk, request.data))
