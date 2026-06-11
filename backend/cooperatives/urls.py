from django.urls import path

from .views import CooperativeDetailView, CooperativeListCreateView, JoinCooperativeView

urlpatterns = [
    path("", CooperativeListCreateView.as_view()),
    path("<int:pk>/", CooperativeDetailView.as_view()),
    path("<int:pk>/join/", JoinCooperativeView.as_view()),
]
