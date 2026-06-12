from django.urls import path

from .csv_views import ParcelCSVExportView
from .geo_views import GeoJSONExportView, GeoJSONImportView, MeasureView
from .history_views import ParcelHistoryView
from .qr_views import ParcelQRVerifyView, ParcelQRView
from .views import NearbyParcelsView, ParcelDetailView, ParcelListCreateView

urlpatterns = [
    path("", ParcelListCreateView.as_view(), name="parcel-list"),
    path("nearby/", NearbyParcelsView.as_view(), name="parcel-nearby"),
    path("export/geojson/", GeoJSONExportView.as_view()),
    path("export/csv/", ParcelCSVExportView.as_view()),
    path("import/geojson/", GeoJSONImportView.as_view()),
    path("measure/", MeasureView.as_view()),
    path("<int:pk>/history/", ParcelHistoryView.as_view()),
    path("<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
    path("<int:pk>/qr/", ParcelQRView.as_view()),
    path("verify/<str:code>/", ParcelQRVerifyView.as_view()),
]
