from datetime import date, timedelta

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from farm_ops.models import FarmTask, FieldJournal
from parcels.models import Parcel

KNOWLEDGE = {
    "semis": "Semez après les premières pluies. Espacement adapté à la culture.",
    "irrigation": "Arrosez tôt le matin (5h-7h). Surveillez l'humidité du sol.",
    "ravageurs": "Inspectez les cultures chaque semaine. Pièges à phéromones recommandés.",
    "sécheresse": "Mulchage, irrigation goutte-à-goutte, cultures résistantes.",
    "engrais": "NPK selon culture — consultez le calendrier cultural ARCA-GIS.",
}


def _parcel_context(user, parcel_id=None):
    parcels = Parcel.objects.filter(owner=user, is_active=True)
    if parcel_id:
        parcels = parcels.filter(pk=parcel_id)
    ctx = []
    for p in parcels[:5]:
        c = p.geometry.centroid if p.geometry else None
        ctx.append({
            "id": p.id,
            "name": p.name,
            "crop": p.crop_type,
            "health": p.health_status,
            "moisture": p.soil_moisture,
            "area_ha": p.area_hectares,
            "lat": c.y if c else None,
            "lng": c.x if c else None,
        })
    return ctx


def _fallback_chat(query, context, language="fr"):
    q = query.lower()
    answers = []
    for key, answer in KNOWLEDGE.items():
        if key in q:
            answers.append({"topic": key, "answer": answer})
    if context.get("parcels"):
        p = context["parcels"][0]
        answers.insert(0, {
            "topic": p["name"],
            "answer": (
                f"Parcelle {p['name']} ({p['crop']}): humidité {p['moisture']}%, "
                f"santé {p['health']}. "
                + ("Irrigation recommandée." if (p["moisture"] or 0) < 40 else "Conditions correctes.")
            ),
        })
    if not answers:
        answers.append({"topic": "general", "answer": "Consultez votre agent agricole ou analysez vos parcelles dans ARCA-GIS."})
    text = " ".join(a["answer"] for a in answers[:2])
    return {"query": query, "language": language, "response": text, "answers": answers, "source": "fallback"}


def _fallback_disease(crop_type):
    return {
        "crop_type": crop_type,
        "diagnosis": {"id": "healthy", "name": "Analyse locale — plante probablement saine", "severity": "none"},
        "confidence": 0.7,
        "treatment": "Surveillance hebdomadaire recommandée.",
        "prevention": "Rotation des cultures, semences certifiées.",
        "source": "fallback",
    }


def _fallback_planner(parcel):
    actions = []
    if (parcel.soil_moisture or 50) < 40:
        actions.append({"action": "irrigate", "when": "demain 06:00", "priority": "high", "label": "Irriguer la parcelle"})
    actions.append({"action": "inspect", "when": (date.today() + timedelta(days=2)).isoformat(), "priority": "medium", "label": "Inspection ravageurs"})
    actions.append({"action": "journal", "when": date.today().isoformat(), "priority": "low", "label": "Noter observations au journal"})
    return {"planned_actions": actions, "source": "fallback"}


class AdvisorChatView(APIView):
    """Conseiller agricole contextuel (parcelles de l'utilisateur)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "query requis"}, status=400)
        language = request.data.get("language", "fr")
        parcel_id = request.data.get("parcel_id")
        context = {"parcels": _parcel_context(request.user, parcel_id)}

        try:
            resp = requests.post(
                f"{settings.AI_MODULE_URL}/rag",
                json={"query": query, "language": language, "context": context},
                timeout=10,
            )
            data = resp.json()
            if resp.status_code >= 400 or "answers" not in data:
                raise requests.RequestException()
            text = " ".join(a["answer"] for a in data.get("answers", [])[:2])
            return Response({**data, "response": text, "context": context})
        except requests.RequestException:
            return Response(_fallback_chat(query, context, language))


class DiseaseDetectView(APIView):
    """Diagnostic maladie par photo (proxy IA)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        crop_type = request.data.get("crop_type", "maize")
        image_b64 = request.data.get("image_b64")
        if not image_b64:
            return Response({"error": "image_b64 requis"}, status=400)
        try:
            resp = requests.post(
                f"{settings.AI_MODULE_URL}/disease-detect",
                json={"image_b64": image_b64, "crop_type": crop_type},
                timeout=15,
            )
            data = resp.json()
            if resp.status_code >= 400 or "diagnosis" not in data:
                raise requests.RequestException()
            return Response(data)
        except requests.RequestException:
            return Response(_fallback_disease(crop_type))


class WeeklyPlannerView(APIView):
    """Planificateur hebdomadaire basé sur parcelles + tâches."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        parcel_id = request.query_params.get("parcel")
        parcels = Parcel.objects.filter(owner=user, is_active=True)
        if parcel_id:
            parcels = parcels.filter(pk=parcel_id)

        today = timezone.now().date()
        week_end = today + timedelta(days=7)
        pending_tasks = FarmTask.objects.filter(
            owner=user,
            status=FarmTask.Status.PENDING,
            due_date__lte=week_end,
        ).order_by("due_date")[:10]

        parcel_plans = []
        for p in parcels[:3]:
            c = p.geometry.centroid if p.geometry else None
            plan_data = _fallback_planner(p)
            if c:
                try:
                    resp = requests.post(
                        f"{settings.AI_MODULE_URL}/autonomous-agent",
                        json={
                            "lat": c.y, "lng": c.x,
                            "crop_type": p.crop_type,
                            "soil_moisture": p.soil_moisture or 50,
                        },
                        timeout=10,
                    )
                    if resp.status_code < 400 and "planned_actions" in resp.json():
                        plan_data = resp.json()
                except requests.RequestException:
                    pass
            parcel_plans.append({
                "parcel_id": p.id,
                "parcel_name": p.name,
                "crop": p.crop_type,
                "moisture": p.soil_moisture,
                "actions": plan_data.get("planned_actions", []),
                "source": plan_data.get("source", plan_data.get("agent", "ai")),
            })

        task_items = [{
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date.isoformat(),
            "status": t.status,
            "parcel": t.parcel.name if t.parcel else None,
        } for t in pending_tasks]

        return Response({
            "week_start": today.isoformat(),
            "week_end": week_end.isoformat(),
            "parcel_plans": parcel_plans,
            "pending_tasks": task_items,
            "summary": f"{len(parcel_plans)} parcelle(s), {len(task_items)} tâche(s) cette semaine",
        })


class VoiceJournalView(APIView):
    """Transcription vocale → journal de champ."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get("text", "").strip()
        audio_b64 = request.data.get("audio_b64")
        language = request.data.get("language", "fr")
        save = request.data.get("save", True)
        parcel_id = request.data.get("parcel_id")

        if audio_b64 and not text:
            try:
                resp = requests.post(
                    f"{settings.AI_MODULE_URL}/whisper",
                    json={"audio_b64": audio_b64, "language": language},
                    timeout=10,
                )
                if resp.status_code < 400:
                    text = resp.json().get("transcript", text)
            except requests.RequestException:
                pass

        if not text:
            return Response({"error": "text ou audio_b64 requis"}, status=400)

        saved = False
        journal_id = None
        if save:
            parcel = None
            if parcel_id:
                parcel = Parcel.objects.filter(pk=parcel_id, owner=request.user).first()
            entry = FieldJournal.objects.create(
                author=request.user,
                parcel=parcel,
                entry_date=date.today(),
                observation=text,
                weather_note="Saisie vocale IA",
            )
            saved = True
            journal_id = entry.id

        return Response({
            "transcript": text,
            "saved": saved,
            "journal_id": journal_id,
            "language": language,
        })
