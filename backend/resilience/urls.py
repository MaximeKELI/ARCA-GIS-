from django.urls import path

from .views import DroughtEWSView, EarlyWarningListView, FloodSimulationView, RadioHFListView, RefugeListView

urlpatterns = [
    path("refuges/", RefugeListView.as_view()),
    path("early-warnings/", EarlyWarningListView.as_view()),
    path("drought-ews/", DroughtEWSView.as_view()),
    path("flood-simulate/", FloodSimulationView.as_view()),
    path("radio-hf/", RadioHFListView.as_view()),
]
