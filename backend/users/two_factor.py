import base64
import io

import pyotp
import qrcode


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_totp_uri(user, secret: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email or user.username,
        issuer_name="ARCA-GIS",
    )


def generate_qr_base64(uri: str) -> str:
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def verify_totp(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)
