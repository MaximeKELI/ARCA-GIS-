import hashlib
import json

from django.utils import timezone

from .models import AuditLog


def log_immutable(user, action: str, resource: str, resource_id: str, details: dict) -> dict:
    """Audit log avec hash chaîné pour immuabilité."""
    last = AuditLog.objects.order_by("-created_at").first()
    prev_hash = getattr(last, "_chain_hash", "") if last else ""
    payload = json.dumps({
        "action": action, "resource": resource, "resource_id": resource_id,
        "details": details, "prev": prev_hash, "ts": timezone.now().isoformat(),
    }, sort_keys=True)
    chain_hash = hashlib.sha256(payload.encode()).hexdigest()
    log = AuditLog.objects.create(
        user=user, action=action, resource=resource,
        resource_id=resource_id, details={**details, "_chain_hash": chain_hash},
    )
    log._chain_hash = chain_hash
    return {"id": log.id, "chain_hash": chain_hash}
