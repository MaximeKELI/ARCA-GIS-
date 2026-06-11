from django.urls import path

from .views import MarketPriceListView, MarketSeedView

urlpatterns = [
    path("prices/", MarketPriceListView.as_view()),
    path("seed/", MarketSeedView.as_view()),
]
