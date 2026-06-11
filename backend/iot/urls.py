from django.urls import path

from .extension_views import BuoyIngestView, PestTrapIngestView
from .views import SensorIngestView, SensorListView, SensorReadingListView

urlpatterns = [
    path("sensors/", SensorListView.as_view()),
    path("sensors/<int:sensor_id>/readings/", SensorReadingListView.as_view()),
    path("ingest/", SensorIngestView.as_view()),
    path("buoys/ingest/", BuoyIngestView.as_view()),
    path("pest-traps/ingest/", PestTrapIngestView.as_view()),
]
