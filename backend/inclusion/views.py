import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NutritionRecord, VillageWhatsAppGroup, WomenFarmerProgram


class VillageGroupListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VillageWhatsAppGroup.objects.filter(alerts_enabled=True)

    def list(self, request, *args, **kwargs):
        return Response([{
            "village": g.village_name, "region": g.region, "members": g.member_count,
        } for g in self.get_queryset()])


class WomenProgramListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WomenFarmerProgram.objects.filter(participant=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response([{
            "cooperative": p.cooperative, "hectares": p.hectares_managed,
            "income": float(p.income_xof), "trainings": p.training_completed,
        } for p in self.get_queryset()])

    def create(self, request, *args, **kwargs):
        p = WomenFarmerProgram.objects.create(
            participant=request.user,
            cooperative=request.data.get("cooperative", ""),
            hectares_managed=request.data.get("hectares_managed", 0),
        )
        return Response({"id": p.id}, status=201)


class NutritionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NutritionRecord.objects.filter(recorded_by=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response([{
            "child": n.child_name, "age_months": n.age_months,
            "risk": n.malnutrition_risk, "food_sources": n.food_sources,
        } for n in self.get_queryset()])

    def create(self, request, *args, **kwargs):
        n = NutritionRecord.objects.create(
            recorded_by=request.user,
            child_name=request.data.get("child_name"),
            age_months=request.data.get("age_months", 24),
            region=request.data.get("region", request.user.region),
            malnutrition_risk=request.data.get("malnutrition_risk", "low"),
            food_sources=request.data.get("food_sources", []),
        )
        return Response({"id": n.id}, status=201)


class VoiceTranslateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            resp = requests.post(f"{settings.AI_MODULE_URL}/voice-translate", json=request.data, timeout=10)
            return Response(resp.json())
        except requests.RequestException:
            return Response({
                "text": request.data.get("text", ""),
                "target_language": request.data.get("target_language", "bm"),
                "translated": request.data.get("text", ""),
                "audio_url": None,
                "source": "fallback",
            })


class PictogramMenuView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "items": [
                {"id": "sos", "icon": "warning", "label": "SOS", "audio": "Urgence"},
                {"id": "weather", "icon": "cloud", "label": "Météo", "audio": "Météo"},
                {"id": "parcels", "icon": "grass", "label": "Champs", "audio": "Mes parcelles"},
                {"id": "market", "icon": "store", "label": "Marché", "audio": "Prix marché"},
                {"id": "water", "icon": "water", "label": "Eau", "audio": "Eau"},
                {"id": "help", "icon": "phone", "label": "Aide", "audio": "Appeler aide"},
            ],
        })
