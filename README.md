# Agent Planificateur pour Optimisation d'Énergie (Master Project)

## Résumé
Application full-stack (Python + React + MySQL) qui aide un utilisateur (maison ou bâtiment) à :
- modéliser la consommation énergétique à partir des **équipements** (lampes, clim, etc.)
- intégrer un scénario **solaire** (panneaux) pour réduire la consommation réseau
- estimer les **économies**, le **temps de rentabilité** (payback) et le gain net sur 3/5 ans
- proposer des **recommandations** (LED, planification, isolation, usage clim)

## Données d'entrée (exemples)
- Nombre de lampes, puissance (W), heures (soir, etc.)
- Équipements électriques : clim, frigo, TV, chauffe-eau...
- Type de localisation : `countryside` / `village` / `city` (utilisé pour adapter les recommandations)
- Tarifs électricité par période (matin/midi/soir/nuit)
- Configuration solaire : taille kWp, coût, PSH, PR

## Méthode (académique)
Le modèle calcule la consommation par période (matin/midi/soir/nuit) et applique le solaire
principalement sur la période **midi**, ce qui correspond au cas d'usage : alimenter la clim
par le solaire en journée.

### Formules
- `kWh = (W × heures × quantité) / 1000`
- `kWh_mois ≈ kWh_jour × (4.345 × jours_par_semaine)`
- `Prod_mois ≈ kWp × PSH × PR × 30`
- `Payback(années) = coût_installation / économies_annuelles`

## Lancement
Voir `backend/README.md` et `frontend/README.md`.

## Extensions possibles (pour mémoire Master)
- Facturation dynamique : heures pleines/creuses réelles
- Batterie (stockage) pour couvrir le soir
- Prise en compte météo/irradiation via API (PVGIS, etc.)
- Modèle CO2 (kgCO2/kWh) + reporting ESG
"# devop" 
