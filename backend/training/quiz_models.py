from django.conf import settings
from django.db import models


class Quiz(models.Model):
    course = models.ForeignKey("training.Course", on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    pass_score = models.PositiveIntegerField(default=70)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_index = models.PositiveIntegerField(default=0)


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)


class TrainingCertificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("training.Course", on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
