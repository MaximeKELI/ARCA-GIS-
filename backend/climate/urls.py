from django.urls import path

from .calendar_views import CropCalendarListView, CurrentSeasonView
from .irrigation_views import IrrigationAdviceView
from .views import (
    AIAnalysisView,
    ClimateEventDetailView,
    ClimateEventListCreateView,
    NearbyClimateEventsView,
    WeatherCurrentView,
    WeatherForecastView,
    WeatherReadingListView,
    WeatherStationListView,
)

urlpatterns = [
    path("events/", ClimateEventListCreateView.as_view(), name="climate-events"),
    path("events/nearby/", NearbyClimateEventsView.as_view(), name="climate-events-nearby"),
    path("events/<int:pk>/", ClimateEventDetailView.as_view(), name="climate-event-detail"),
    path("analyze/", AIAnalysisView.as_view(), name="climate-analyze"),
    path("weather/current/", WeatherCurrentView.as_view()),
    path("weather/forecast/", WeatherForecastView.as_view()),
    path("stations/", WeatherStationListView.as_view(), name="weather-stations"),
    path("readings/", WeatherReadingListView.as_view(), name="weather-readings"),
    path("calendar/", CropCalendarListView.as_view()),
    path("calendar/current/", CurrentSeasonView.as_view()),
    path("irrigation/advice/", IrrigationAdviceView.as_view()),
]
