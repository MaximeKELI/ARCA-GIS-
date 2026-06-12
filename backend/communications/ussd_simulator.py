"""Simulateur USSD interne — pas de passerelle externe."""

MENU = {
    "": "Bienvenue ARCA-GIS\n1. SOS\n2. Meteo\n3. Parcelles\n4. Prix marche",
    "1": "SOS active. Secours alerte.\n0. Retour",
    "2": "Meteo: 28C, pluie 10%.\n0. Retour",
    "3": "Vos parcelles: consultez l'app.\n0. Retour",
    "4": "Maïs: 250 XOF/kg.\n0. Retour",
}


def simulate_ussd(session_id: str, phone: str, text: str) -> str:
    parts = text.split("*") if text else [""]
    key = parts[-1] if parts else ""
    if key == "0":
        key = ""
    response = MENU.get(key, "Option invalide.\n0. Retour")
    return f"CON {response}" if not key.startswith("1") or key == "1" else f"END {response}"
