from django.urls import path

from .views import CourseListView, CourseProgressView, MyProgressView

urlpatterns = [
    path("courses/", CourseListView.as_view()),
    path("courses/<int:pk>/progress/", CourseProgressView.as_view()),
    path("my-progress/", MyProgressView.as_view()),
]
