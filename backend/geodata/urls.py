from django.urls import path

from .views import CommunityPointListCreateView, WMSLayerListView

urlpatterns = [
    path("community-points/", CommunityPointListCreateView.as_view()),
    path("wms-layers/", WMSLayerListView.as_view()),
]
