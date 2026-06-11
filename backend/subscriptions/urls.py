from django.urls import path

from .views import MySubscriptionView, PlanListView

urlpatterns = [
    path("plans/", PlanListView.as_view()),
    path("my/", MySubscriptionView.as_view()),
]
