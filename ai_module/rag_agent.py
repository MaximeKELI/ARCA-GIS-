"""Agent IA conversationnel avec base de connaissances agronomique."""

KNOWLEDGE = {
    "semis maïs": "Semez le maïs après les premières pluies, espacement 75cm x 25cm, 2-3 graines par poquet.",
    "irrigation": "Arrosez tôt le matin (5h-7h). Le maïs nécessite 500-800mm par cycle.",
    "ravageurs": "Inspectez les cultures chaque semaine. Utilisez des pièges à phéromones.",
    "sécheresse": "Mulchage, irrigation goutte-à-goutte, cultures résistantes (niébé, sorgho).",
    "riz": "Le riz nécessite beaucoup d'eau. Maintenir 5-10cm d'eau dans la rizière.",
    "engrais": "NPK 15-15-15 pour maïs à 200kg/ha, 3 semaines après semis.",
}


def rag_query(query: str, language: str = "fr", context: dict | None = None) -> dict:
    q = query.lower()
    matches = []
    for key, answer in KNOWLEDGE.items():
        if any(word in q for word in key.split()):
            matches.append({"topic": key, "answer": answer})

    if not matches:
        matches.append({
            "topic": "general",
            "answer": "Consultez un agent agricole local ou utilisez l'analyse IA de votre parcelle.",
        })

    return {
        "query": query,
        "language": language,
        "answers": matches[:3],
        "context": context or {},
        "source": "arca_gis_rag_v1",
    }
