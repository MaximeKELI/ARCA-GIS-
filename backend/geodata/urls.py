from django.urls import path

from .v6_views import CadastreLayerView, ElevationProfileView, MapPDFExportView, OpenDataCatalogView, SatelliteTimelapseView
from .views import CommunityPointListCreateView, WMSLayerListView

urlpatterns = [
    path("community-points/", CommunityPointListCreateView.as_view()),
    path("wms-layers/", WMSLayerListView.as_view()),
    path("timelapse/", SatelliteTimelapseView.as_view()),
    path("elevation/", ElevationProfileView.as_view()),
    path("cadastre/", CadastreLayerView.as_view()),
    path("opendata/", OpenDataCatalogView.as_view()),
    path("export-pdf/", MapPDFExportView.as_view()),
]
