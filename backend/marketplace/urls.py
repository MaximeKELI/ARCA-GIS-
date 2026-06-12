from django.urls import path

from .contracts_views import BuyerContractListCreateView, PriceForecastView
from .listings_views import ListingListCreateView, MyListingsView
from .views import MarketPriceListView, MarketSeedView

urlpatterns = [
    path("prices/", MarketPriceListView.as_view()),
    path("seed/", MarketSeedView.as_view()),
    path("listings/", ListingListCreateView.as_view()),
    path("listings/mine/", MyListingsView.as_view()),
    path("contracts/", BuyerContractListCreateView.as_view()),
    path("price-forecast/", PriceForecastView.as_view()),
]
