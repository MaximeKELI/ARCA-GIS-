"""LLM local offline — réponses basées sur règles (remplaçable par Gemma/Llama)."""

RESPONSES = {
    "semis": "Semez après les premières pluies. Espacement 75cm pour le maïs.",
    "eau": "Arrosez tôt le matin. Vérifiez l'humidité du sol avant irrigation.",
    "prix": "Consultez les prix marché dans l'application ARCA-GIS.",
    "sos": "Activez le bouton SOS rouge pour alerter les secours.",
}


def local_llm(prompt: str, language: str = "fr") -> dict:
    prompt_lower = prompt.lower()
    answer = "Je suis l'assistant ARCA-GIS. Posez une question sur l'agriculture, l'eau ou les urgences."
    for key, resp in RESPONSES.items():
        if key in prompt_lower:
            answer = resp
            break
    return {"prompt": prompt, "response": answer, "language": language, "model": "arca-llm-local-v1", "offline": True}
