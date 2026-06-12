from django.db.models.signals import pre_save
from django.dispatch import receiver

from .history_models import ParcelChangeLog
from .models import Parcel

TRACKED_FIELDS = ("soil_moisture", "health_status", "crop_type", "notes", "name")


@receiver(pre_save, sender=Parcel)
def log_parcel_changes(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Parcel.objects.get(pk=instance.pk)
    except Parcel.DoesNotExist:
        return
    for field in TRACKED_FIELDS:
        old_val = getattr(old, field, None)
        new_val = getattr(instance, field, None)
        if old_val != new_val:
            ParcelChangeLog.objects.create(
                parcel=instance,
                changed_by=getattr(instance, "_changed_by", None),
                field_name=field,
                old_value=str(old_val) if old_val is not None else "",
                new_value=str(new_val) if new_val is not None else "",
            )
