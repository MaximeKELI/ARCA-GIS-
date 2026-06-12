from django.urls import path

from .views import (
    AuctionBidView, AuctionListCreateView, CreditScoreView,
    ExportCertificateListCreateView, GroupPurchaseListCreateView, InputPriceListView,
)

urlpatterns = [
    path("auctions/", AuctionListCreateView.as_view()),
    path("auctions/<int:pk>/bid/", AuctionBidView.as_view()),
    path("group-buy/", GroupPurchaseListCreateView.as_view()),
    path("credit-score/", CreditScoreView.as_view()),
    path("exports/", ExportCertificateListCreateView.as_view()),
    path("input-prices/", InputPriceListView.as_view()),
]
