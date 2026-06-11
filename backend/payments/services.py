import uuid

from .models import Payment


def initiate_payment(user, provider: str, amount: float, phone: str, description: str) -> dict:
    reference = f"ARCA-{uuid.uuid4().hex[:12].upper()}"
    payment = Payment.objects.create(
        user=user,
        provider=provider,
        amount=amount,
        phone=phone,
        description=description,
        reference=reference,
    )

    # En production: appeler API Orange Money / MTN MoMo
    provider_urls = {
        "orange_money": "https://api.orange.com/orange-money-webpay/ci/v1/webpayment",
        "mtn_momo": "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",
    }

    return {
        "reference": reference,
        "status": "pending",
        "provider": provider,
        "amount": float(amount),
        "currency": "XOF",
        "payment_id": payment.id,
        "checkout_url": f"/api/payments/checkout/{reference}/",
        "note": f"Intégrer {provider_urls.get(provider, 'API')} en production",
    }


def verify_payment(reference: str) -> dict:
    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        return {"valid": False}
    return {
        "valid": True,
        "reference": payment.reference,
        "status": payment.status,
        "amount": float(payment.amount),
        "provider": payment.provider,
    }
