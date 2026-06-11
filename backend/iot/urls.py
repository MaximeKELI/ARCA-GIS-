from django.urls import path

from .views import SensorIngestView, SensorListView, SensorReadingListView

urlpatterns = [
    path("sensors/", SensorListView.as_view()),
    path("sensors/<int:sensor_id>/readings/", SensorReadingListView.as_view()),
    path("ingest/", SensorIngestView.as_view()),
]
