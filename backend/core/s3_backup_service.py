import json
import logging
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.core import serializers

logger = logging.getLogger(__name__)


def backup_to_s3() -> dict:
    bucket = getattr(settings, "AWS_S3_BACKUP_BUCKET", None)
    access_key = getattr(settings, "AWS_ACCESS_KEY_ID", None)
    secret_key = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)

    if not all([bucket, access_key, secret_key]):
        return {"status": "simulated", "message": "Configurer AWS_S3_BACKUP_BUCKET et clés AWS"}

    try:
        import boto3
        from parcels.models import Parcel
        from users.models import User

        data = serializers.serialize("json", list(User.objects.all()[:100]) + list(Parcel.objects.all()[:500]))
        s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        key = f"backups/arca_gis_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.json"
        s3.upload_fileobj(BytesIO(data.encode()), bucket, key)
        return {"status": "completed", "bucket": bucket, "key": key}
    except ImportError:
        return {"status": "error", "message": "pip install boto3 pour backup S3"}
    except Exception as e:
        logger.warning("S3 backup failed: %s", e)
        return {"status": "failed", "error": str(e)}
