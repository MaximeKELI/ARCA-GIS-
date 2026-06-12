import uuid

from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .certificate_service import generate_certificate_pdf
from .quiz_models import Quiz, QuizAttempt, QuizQuestion, TrainingCertificate


class QuizDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz introuvable"}, status=404)
        return Response({
            "id": quiz.id, "title": quiz.title, "pass_score": quiz.pass_score,
            "questions": [{"id": q.id, "question": q.question, "options": q.options}
                          for q in quiz.questions.all()],
        })


class QuizSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz introuvable"}, status=404)
        answers = request.data.get("answers", {})
        total = quiz.questions.count()
        correct = sum(1 for q in quiz.questions.all() if answers.get(str(q.id)) == q.correct_index)
        score = int(correct / total * 100) if total else 0
        passed = score >= quiz.pass_score
        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score, passed=passed)
        cert_id = None
        if passed:
            cert_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            TrainingCertificate.objects.get_or_create(
                user=request.user, course=quiz.course,
                defaults={"certificate_id": cert_id},
            )
        return Response({"score": score, "passed": passed, "certificate_id": cert_id})


class CertificateDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cert_id):
        try:
            cert = TrainingCertificate.objects.get(certificate_id=cert_id, user=request.user)
        except TrainingCertificate.DoesNotExist:
            return Response({"error": "Certificat introuvable"}, status=404)
        pdf = generate_certificate_pdf(request.user, cert.course, cert.certificate_id)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{cert_id}.pdf"'
        return response
