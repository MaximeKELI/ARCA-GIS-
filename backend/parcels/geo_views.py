import json

from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Parcel
from .serializers import ParcelSerializer


class GeoJSONExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        parcels = Parcel.objects.filter(owner=request.user, is_active=True)
        features = []
        for p in parcels:
            if p.geometry:
                features.append({
                    "type": "Feature",
                    "properties": {"id": p.id, "name": p.name, "crop_type": p.crop_type, "area_ha": p.area_hectares},
                    "geometry": json.loads(p.geometry.geojson),
                })
        geojson = {"type": "FeatureCollection", "features": features}
        response = HttpResponse(json.dumps(geojson), content_type="application/geo+json")
        response["Content-Disposition"] = 'attachment; filename="parcels.geojson"'
        return response


class GeoJSONImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        created = 0
        for feat in data.get("features", []):
            geom = GEOSGeometry(json.dumps(feat["geometry"]), srid=4326)
            props = feat.get("properties", {})
            Parcel.objects.create(
                owner=request.user,
                name=props.get("name", f"Import {created + 1}"),
                crop_type=props.get("crop_type", "maize"),
                geometry=geom,
            )
            created += 1
        return Response({"imported": created}, status=201)


class MeasureView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from django.contrib.gis.geos import LineString, Polygon
        from django.contrib.gis.measure import Distance

        measure_type = request.data.get("type", "distance")
        coords = request.data.get("coordinates", [])

        if measure_type == "distance" and len(coords) >= 2:
            line = LineString([(c[0], c[1]) for c in coords], srid=4326)
            km = line.length * 111
            return Response({"type": "distance", "km": round(km, 3), "m": round(km * 1000, 1)})

        if measure_type == "area" and len(coords) >= 3:
            ring = [(c[0], c[1]) for c in coords]
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            poly = Polygon(ring, srid=4326)
            ha = poly.area * 111320 * 111320 / 10000
            return Response({"type": "area", "hectares": round(ha, 4), "m2": round(ha * 10000, 1)})

        return Response({"error": "coordinates invalides"}, status=400)
