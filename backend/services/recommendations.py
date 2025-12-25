"""Génération de recommandations qualitatives + estimations simples."""
from typing import List, Dict
from .analysis import ApplianceInput

def recommend(location_type: str, appliances: List[ApplianceInput], has_solar: bool) -> List[Dict]:
    tips: List[Dict] = []

    # 1) Lampes -> LED
    lamp_kinds = [a for a in appliances if a.category.lower() in ("lamp", "lighting", "lamps")]
    if lamp_kinds:
        tips.append({
            "title": "Remplacer les lampes par des LED",
            "why": "Les LED consomment souvent 5× à 10× moins pour un flux lumineux équivalent.",
            "how": "Remplacer par des LED 7-12W au lieu de 60W, et ajouter des détecteurs de présence si possible."
        })

    # 2) Climatisation : conseils d'usage
    ac = [a for a in appliances if a.category.lower() in ("ac", "air_conditioner", "climatiseur")]
    if ac:
        if location_type.lower() in ("village", "countryside"):
            tips.append({
                "title": "Optimiser la climatisation selon la plage horaire",
                "why": "La clim est un des plus gros postes de consommation.",
                "how": "Régler 24–26°C, fermer les portes/fenêtres, nettoyer les filtres. Si solaire : utiliser davantage entre 12h-18h."
            })
        if not has_solar:
            tips.append({
                "title": "Solution simple : panneaux solaires pour alimenter la clim en journée",
                "why": "La production solaire est maximale vers midi, ce qui colle bien aux besoins de clim en climat chaud.",
                "how": "Utiliser la clim surtout 12h-18h via le solaire, et limiter matin/soir sur le réseau."
            })

    # 3) Isolation
    tips.append({
        "title": "Réduire les pertes : isolation et étanchéité",
        "why": "Moins de pertes = moins de chauffage/clim.",
        "how": "Joints de fenêtres, rideaux thermiques, isolation toiture/murs si possible."
    })

    # 4) Pilotage intelligent
    tips.append({
        "title": "Planification : programmer les usages",
        "why": "Décaler les consommations vers les heures les moins chères (ou solaires) réduit la facture.",
        "how": "Programmateurs, prises connectées, scénarios (chauffe-eau, lave-linge) en heures creuses ou en journée solaire."
    })

    return tips
