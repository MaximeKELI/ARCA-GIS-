from django.urls import path

from .quiz_views import QuizDetailView, QuizSubmitView
from .views import CourseListView, CourseProgressView, MyProgressView

urlpatterns = [
    path("courses/", CourseListView.as_view()),
    path("courses/<int:pk>/progress/", CourseProgressView.as_view()),
    path("my-progress/", MyProgressView.as_view()),
    path("quizzes/<int:pk>/", QuizDetailView.as_view()),
    path("quizzes/<int:pk>/submit/", QuizSubmitView.as_view()),
]
