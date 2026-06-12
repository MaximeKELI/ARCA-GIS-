from django.urls import path

from .views import (
    BudgetListCreateView, BudgetSummaryView, CropSeasonListCreateView,
    FarmTaskCompleteView, FarmTaskListCreateView, FieldJournalListCreateView,
    GenerateTasksView, HarvestJournalListCreateView, HarvestStatsView,
    InventoryAlertsView, InventoryListCreateView, LoanCalculatorView, ParcelCompareView,
)

urlpatterns = [
    path("seasons/", CropSeasonListCreateView.as_view()),
    path("harvests/", HarvestJournalListCreateView.as_view()),
    path("harvests/stats/", HarvestStatsView.as_view()),
    path("journal/", FieldJournalListCreateView.as_view()),
    path("inventory/", InventoryListCreateView.as_view()),
    path("inventory/alerts/", InventoryAlertsView.as_view()),
    path("tasks/", FarmTaskListCreateView.as_view()),
    path("tasks/<int:pk>/complete/", FarmTaskCompleteView.as_view()),
    path("tasks/generate/", GenerateTasksView.as_view()),
    path("budget/", BudgetListCreateView.as_view()),
    path("budget/summary/", BudgetSummaryView.as_view()),
    path("loan-calculator/", LoanCalculatorView.as_view()),
    path("parcels/compare/", ParcelCompareView.as_view()),
]
