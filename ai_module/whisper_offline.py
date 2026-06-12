"""Transcription vocale offline (stub — remplaçable par Whisper tiny)."""

PHRASES = {
    "fr": {"semis": "Quand semer le maïs", "sos": "Urgence secours"},
    "bm": {"semis": "San kalo waati", "sos": "Dɛmɛnan"},
}


def transcribe_audio(audio_b64: str | None, language: str = "fr") -> dict:
    return {
        "transcript": PHRASES.get(language, PHRASES["fr"]).get("semis", ""),
        "language": language,
        "confidence": 0.85,
        "model": "whisper-tiny-stub",
        "offline": True,
    }


def translate_voice(text: str, target_language: str = "bm") -> dict:
    translations = {
        "bm": f"[Bambara] {text}",
        "wo": f"[Wolof] {text}",
        "ha": f"[Hausa] {text}",
        "dyu": f"[Dioula] {text}",
    }
    return {
        "text": text, "target_language": target_language,
        "translated": translations.get(target_language, text),
        "audio_url": None, "offline": True,
    }
