from django.utils import timezone

from .models import InsuranceClaim, InsurancePolicy


def evaluate_parametric_trigger(policy: InsurancePolicy, weather_data: dict) -> bool:
    """Évalue si les conditions météo déclenchent une indemnisation."""
    threshold = policy.trigger_threshold

    if policy.policy_type == InsurancePolicy.PolicyType.DROUGHT:
        rainfall = weather_data.get("rainfall_mm", 100)
        days = threshold.get("max_rainfall_mm", 20)
        period_days = threshold.get("period_days", 30)
        return rainfall < days

    if policy.policy_type == InsurancePolicy.PolicyType.FLOOD:
        rainfall = weather_data.get("rainfall_mm", 0)
        return rainfall > threshold.get("min_rainfall_mm", 100)

    if policy.policy_type == InsurancePolicy.PolicyType.CROP_FAILURE:
        ndvi = weather_data.get("ndvi_score", 1.0)
        return ndvi < threshold.get("min_ndvi", 0.25)

    return False


def process_claim(policy_id: int, weather_data: dict) -> dict:
    try:
        policy = InsurancePolicy.objects.get(pk=policy_id, is_active=True)
    except InsurancePolicy.DoesNotExist:
        return {"error": "Police introuvable"}

    triggered = evaluate_parametric_trigger(policy, weather_data)
    if not triggered:
        return {"triggered": False, "policy_id": policy_id}

    claim = InsuranceClaim.objects.create(
        policy=policy,
        status=InsuranceClaim.Status.TRIGGERED,
        trigger_data=weather_data,
        payout_amount=policy.coverage_amount,
        triggered_at=timezone.now(),
    )
    return {
        "triggered": True,
        "claim_id": claim.id,
        "payout_amount": float(policy.coverage_amount),
        "policy_type": policy.policy_type,
    }
