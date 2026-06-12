from datetime import date, timedelta

from climate.models import CropCalendar

from .models import FarmTask


def generate_tasks_from_calendar(user) -> int:
    today = date.today()
    region = user.region or "Bouaké"
    created = 0
    for cal in CropCalendar.objects.filter(region=region):
        if cal.planting_start <= today.strftime("%m-%d") <= cal.planting_end:
            _, was_created = FarmTask.objects.get_or_create(
                owner=user, title=f"Semis {cal.crop_name}", due_date=today + timedelta(days=7),
                defaults={"crop_type": cal.crop_type, "source": "calendar",
                          "description": cal.tips or "Période de semis recommandée"},
            )
            if was_created:
                created += 1
        for i, treatment in enumerate(cal.treatments[:2]):
            _, was_created = FarmTask.objects.get_or_create(
                owner=user, title=f"Traitement: {treatment}", due_date=today + timedelta(days=14 + i * 7),
                defaults={"crop_type": cal.crop_type, "source": "phytosanitary"},
            )
            if was_created:
                created += 1
    return created
