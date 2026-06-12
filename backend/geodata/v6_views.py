from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class SatelliteTimelapseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        frames = []
        for month in range(1, 13):
            frames.append({
                "month": month, "ndvi": round(0.3 + (month % 6) * 0.1, 2),
                "label": f"2025-{month:02d}",
            })
        return Response({"lat": lat, "lng": lng, "frames": frames, "source": "sentinel_sim"})


class ElevationProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = float(request.query_params.get("lat", 7.69))
        lng = float(request.query_params.get("lng", -5.03))
        elevation = 200 + (abs(lat * 100) % 150)
        slope = round((elevation % 30) / 10, 1)
        return Response({
            "elevation_m": elevation, "slope_deg": slope,
            "erosion_risk": "high" if slope > 2 else "low",
            "lat": lat, "lng": lng,
        })


class CadastreLayerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "layers": [
                {"name": "Parcelles cadastrales", "source": "IGN-CI", "available": False},
                {"name": "Limites administratives", "source": "OpenStreetMap", "available": True},
            ],
            "note": "Intégrer données cadastrales officielles par pays",
        })


class OpenDataCatalogView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "datasets": [
                {"name": "FAOSTAT Production", "url": "https://www.fao.org/faostat/", "format": "CSV"},
                {"name": "FEWS NET Africa", "url": "https://fews.net/", "format": "GeoJSON"},
                {"name": "World Bank Ag Indicators", "url": "https://data.worldbank.org/", "format": "API"},
            ],
        })


class MapPDFExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buf = BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            c.drawString(50, 800, "ARCA-GIS — Carte parcelles")
            c.drawString(50, 780, f"Région: {request.data.get('region', 'N/A')}")
            c.drawString(50, 760, f"Parcelles: {request.data.get('parcel_count', 0)}")
            c.save()
            response = HttpResponse(buf.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="arca_map.pdf"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)
