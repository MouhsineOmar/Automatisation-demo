# Backend (Flask) — Agent Planificateur Énergie

## Ce que fait le backend
- Stocke un **profil** (type de localisation, tarifs kWh par période, monnaie)
- Stocke des **appareils** (puissance, quantité, heures d'usage par période)
- Optionnel : stocke une config **solaire** (kWp, coût, PSH, PR)
- Calcule :
  - consommation (kWh/mois) par période et totale
  - coût (monnaie/mois) par période et total
  - impact du solaire (autoconsommation, surplus)
  - économies et **temps de rentabilité** (payback) + gains nets sur 3/5 ans
  - recommandations de réduction de consommation

## Formules clés (académiques)
- **Énergie d’un appareil** : `kWh = (W × heures × quantité) / 1000`
- **Mensualisation** : `kWh_mois ≈ kWh_jour × (4.345 × jours_par_semaine)`
- **Production solaire** : `Prod_mois ≈ kWp × PSH × PR × 30`
- **Rentabilité** : `Payback(années) = coût_installation / économies_annuelles`

## Installation (Windows / XAMPP)
1) Créer une base MySQL :
   ```sql
   CREATE DATABASE energy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2) Dans `backend/` :
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3) Lancer l'application :
   - Option 1 (simple) : **depuis `backend/`**
     ```bash
     python app.py
     ```
   - Option 2 (package) : **depuis la racine**
     ```bash
     python -m backend.app
     ```

## Données démo
Créez un profil démo (lampes + clim + frigo + solaire) :
```bash
python populate_demo.py
```
Puis testez :
- GET `http://localhost:5000/api/profiles`
- GET `http://localhost:5000/api/profiles/<id>/analysis`
