"""Assistant vocal multilingue pour conseils agricoles."""

ADVICE_TEMPLATES = {
    "fr": {
        "drought": "Attention, risque de sécheresse. Arrosez vos cultures tôt le matin.",
        "flood": "Fortes pluies prévues. Améliorez le drainage de vos champs.",
        "good": "Conditions favorables. Continuez vos pratiques actuelles.",
        "pest": "Surveillez les ravageurs. Traitez préventivement si nécessaire.",
        "greeting": "Bonjour, je suis l'assistant ARCA-GIS. Comment puis-je vous aider?",
    },
    "en": {
        "drought": "Warning, drought risk. Water your crops early in the morning.",
        "flood": "Heavy rain expected. Improve field drainage.",
        "good": "Favorable conditions. Continue current practices.",
        "pest": "Watch for pests. Apply preventive treatment if needed.",
        "greeting": "Hello, I am the ARCA-GIS assistant. How can I help?",
    },
    "sw": {
        "drought": "Tahadhari, hatari ya ukame. Nyunyuzia mazao yako asubuhi na mapema.",
        "flood": "Mvua kubwa inatarajiwa. Boresha mifereji ya shamba.",
        "good": "Hali nzuri. Endelea na mazoea yako ya sasa.",
        "pest": "Angalia wadudu. Tiba kinga ikiwa ni lazima.",
        "greeting": "Habari, mimi ni msaidizi wa ARCA-GIS. Naweza kukusaidia vipi?",
    },
    "bm": {
        "drought": "A tigɛ, jiɲɛ bagan. Ji caman di sɔgɔma dunanya waati la.",
        "flood": "Sanji be se ka caya. I ka foro ji bɔnɛ labɛn.",
        "good": "Baganw ɲɛ. I ka baara daminɛ cogo la.",
        "pest": "Kɔnɔw lajɛ. Furakɛli kɛ ni a ɲɛna.",
        "greeting": "I ni ce, ne ye ARCA-GIS dɛmɛbaga ye.",
    },
}


def get_voice_response(query: str, language: str = "fr", context: dict | None = None) -> dict:
    templates = ADVICE_TEMPLATES.get(language, ADVICE_TEMPLATES["fr"])
    query_lower = query.lower()

    if any(w in query_lower for w in ["sécheresse", "drought", "ukame", "jiɲɛ"]):
        response = templates["drought"]
    elif any(w in query_lower for w in ["inondation", "flood", "mvua", "sanji"]):
        response = templates["flood"]
    elif any(w in query_lower for w in ["ravageur", "pest", "wadudu", "kɔnɔ"]):
        response = templates["pest"]
    elif any(w in query_lower for w in ["bonjour", "hello", "habari", "i ni ce"]):
        response = templates["greeting"]
    else:
        response = templates["good"]

    if context and context.get("recommendations"):
        response += " " + context["recommendations"][0]

    return {
        "query": query,
        "response": response,
        "language": language,
        "format": "text",
        "audio_note": "Utiliser gTTS ou Polly pour synthèse audio",
    }
