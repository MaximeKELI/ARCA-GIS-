from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExportCertificate, FarmerCreditScore, GroupPurchase, InputPrice, LiveAuction


class AuctionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LiveAuction.objects.filter(status=LiveAuction.Status.LIVE)

    def list(self, request, *args, **kwargs):
        data = [{
            "id": a.id, "crop_type": a.crop_type, "quantity_kg": a.quantity_kg,
            "starting_price": float(a.starting_price),
            "current_bid": float(a.current_bid) if a.current_bid else None,
            "ends_at": a.ends_at.isoformat(),
        } for a in self.get_queryset()]
        return Response(data)

    def create(self, request, *args, **kwargs):
        from datetime import timedelta
        a = LiveAuction.objects.create(
            seller=request.user,
            crop_type=request.data.get("crop_type"),
            quantity_kg=request.data.get("quantity_kg"),
            starting_price=request.data.get("starting_price"),
            ends_at=timezone.now() + timedelta(hours=2),
        )
        return Response({"id": a.id, "status": "live"}, status=201)


class AuctionBidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            auction = LiveAuction.objects.get(pk=pk, status=LiveAuction.Status.LIVE)
        except LiveAuction.DoesNotExist:
            return Response({"error": "Enchère introuvable"}, status=404)
        bid = float(request.data.get("amount", 0))
        if auction.current_bid and bid <= float(auction.current_bid):
            return Response({"error": "Enchère trop basse"}, status=400)
        auction.current_bid = bid
        auction.highest_bidder = request.user
        auction.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"auction_{pk}",
            {"type": "auction.bid", "amount": bid, "bidder": request.user.username},
        )
        return Response({"current_bid": bid, "bidder": request.user.username})


class GroupPurchaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroupPurchase.objects.filter(is_open=True)

    def list(self, request, *args, **kwargs):
        return Response([{
            "id": g.id, "product": g.product, "product_type": g.product_type,
            "target_kg": g.target_quantity_kg, "current_kg": g.current_quantity_kg,
            "unit_price": float(g.unit_price), "region": g.region,
        } for g in self.get_queryset()])

    def create(self, request, *args, **kwargs):
        from datetime import timedelta
        deadline = request.data.get("deadline")
        if not deadline:
            deadline = (timezone.now() + timedelta(days=30)).date()
        g = GroupPurchase.objects.create(
            organizer=request.user,
            product=request.data.get("product"),
            product_type=request.data.get("product_type", "fertilizer"),
            target_quantity_kg=request.data.get("target_quantity_kg", 1000),
            unit_price=request.data.get("unit_price", 500),
            region=request.data.get("region", request.user.region),
            deadline=deadline,
        )
        return Response({"id": g.id}, status=201)


class CreditScoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        score, _ = FarmerCreditScore.objects.get_or_create(farmer=request.user)
        return Response({"score": score.score, "grade": score.grade,
                         "harvests_on_time": score.harvests_on_time, "loans_repaid": score.loans_repaid})


class ExportCertificateListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExportCertificate.objects.filter(exporter=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response([{
            "id": c.id, "crop_type": c.crop_type, "destination": c.destination_country,
            "phytosanitary_cert": c.phytosanitary_cert, "status": c.status,
        } for c in self.get_queryset()])

    def create(self, request, *args, **kwargs):
        import uuid
        c = ExportCertificate.objects.create(
            exporter=request.user,
            crop_type=request.data.get("crop_type"),
            quantity_kg=request.data.get("quantity_kg"),
            destination_country=request.data.get("destination_country"),
            phytosanitary_cert=f"PHY-{uuid.uuid4().hex[:8].upper()}",
        )
        return Response({"id": c.id, "cert": c.phytosanitary_cert}, status=201)


class InputPriceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = InputPrice.objects.all()
        region = self.request.query_params.get("region")
        if region:
            qs = qs.filter(region=region)
        return qs[:50]

    def list(self, request, *args, **kwargs):
        return Response([{
            "product": p.product, "type": p.product_type, "region": p.region,
            "price": float(p.price_per_unit), "unit": p.unit,
        } for p in self.get_queryset()])
