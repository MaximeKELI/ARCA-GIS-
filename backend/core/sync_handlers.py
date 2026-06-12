from django.contrib.gis.geos import Point
from django.utils import timezone

from farm_ops.models import FarmTask, FieldJournal, HarvestJournal
from parcels.models import Parcel


def process_offline_item(item) -> bool:
    """Traite un élément de la file offline. Retourne True si synchronisé."""
    data = item.payload
    user = item.user

    if item.action_type == "sos":
        from incidents.models import Incident
        Incident.objects.create(
            reporter=user, incident_type=Incident.IncidentType.SOS,
            title="SOS (sync hors-ligne)", description=data.get("description", ""),
            location=Point(data["lng"], data["lat"], srid=4326), is_sos=True,
        )
        return True

    if item.action_type == "harvest":
        parcel_id = data.get("parcel_id") or Parcel.objects.filter(owner=user).values_list("pk", flat=True).first()
        if not parcel_id:
            return False
        HarvestJournal.objects.create(
            owner=user, parcel_id=parcel_id,
            crop_type=data.get("crop_type", "maize"),
            quantity_kg=data["quantity_kg"],
            harvest_date=data.get("harvest_date", timezone.now().date()),
        )
        return True

    if item.action_type == "journal":
        FieldJournal.objects.create(
            author=user, parcel_id=data.get("parcel_id"),
            entry_date=data["entry_date"], observation=data["observation"],
            weather_note=data.get("weather_note", ""),
        )
        return True

    if item.action_type == "task_complete":
        FarmTask.objects.filter(pk=data["task_id"], owner=user).update(status="done")
        return True

    if item.action_type == "parcel_update":
        Parcel.objects.filter(pk=data["parcel_id"], owner=user).update(
            **{k: v for k, v in data.items() if k in ("soil_moisture", "health_status", "notes")}
        )
        return True

    return False
