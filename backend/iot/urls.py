from django.urls import path

from .extension_views import BuoyIngestView, PestTrapIngestView
from .v6_views import EdgeAIIngestView, LoRaIngestView, OTAFirmwareView, RainGaugeIngestView, SoilStationIngestView
from .views import SensorIngestView, SensorListView, SensorReadingListView

urlpatterns = [
    path("sensors/", SensorListView.as_view()),
    path("sensors/<int:sensor_id>/readings/", SensorReadingListView.as_view()),
    path("ingest/", SensorIngestView.as_view()),
    path("buoys/ingest/", BuoyIngestView.as_view()),
    path("pest-traps/ingest/", PestTrapIngestView.as_view()),
    path("lora/ingest/", LoRaIngestView.as_view()),
    path("soil-stations/ingest/", SoilStationIngestView.as_view()),
    path("rain-gauges/ingest/", RainGaugeIngestView.as_view()),
    path("ota/", OTAFirmwareView.as_view()),
    path("edge-ai/ingest/", EdgeAIIngestView.as_view()),
]
