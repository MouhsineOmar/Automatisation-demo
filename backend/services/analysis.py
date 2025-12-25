"""Moteur de calcul (formules) : consommation, coût, solaire, économies, ROI."""
from dataclasses import dataclass
from typing import Dict, List, Tuple

PERIODS = ["morning", "midday", "evening", "night"]

@dataclass
class ApplianceInput:
    name: str
    category: str
    power_watts: float
    quantity: int
    h_morning: float
    h_midday: float
    h_evening: float
    h_night: float
    days_per_week: int = 7

def kwh(power_watts: float, hours: float, quantity: int = 1) -> float:
    # kWh = (W * h * qty) / 1000
    return (power_watts * hours * quantity) / 1000.0

def month_factor(days_per_week: int) -> float:
    # approx: semaines/mois = 4.345
    return 4.345 * max(0, min(days_per_week, 7))

def compute_load_by_period_month(appliances: List[ApplianceInput]) -> Dict[str, float]:
    """Retourne la conso mensuelle (kWh) par période."""
    loads = {p: 0.0 for p in PERIODS}
    for a in appliances:
        mf = month_factor(a.days_per_week)
        loads["morning"] += kwh(a.power_watts, a.h_morning, a.quantity) * mf
        loads["midday"]  += kwh(a.power_watts, a.h_midday,  a.quantity) * mf
        loads["evening"] += kwh(a.power_watts, a.h_evening, a.quantity) * mf
        loads["night"]   += kwh(a.power_watts, a.h_night,   a.quantity) * mf
    return loads

def compute_cost(loads_kwh: Dict[str, float], prices: Dict[str, float]) -> float:
    return sum(loads_kwh[p] * prices[p] for p in PERIODS)

def solar_production_month(system_kwp: float, peak_sun_hours_midday: float, performance_ratio: float) -> float:
    # Production/jour ≈ kWp * PSH * PR ; Production/mois ≈ * 30
    return max(0.0, system_kwp) * max(0.0, peak_sun_hours_midday) * max(0.0, min(performance_ratio, 1.0)) * 30.0

def analyze(appliances: List[ApplianceInput], prices: Dict[str, float],
            solar_kwp: float, solar_cost: float, psh_midday: float, pr: float) -> Dict:
    """Analyse complète + formules."""
    loads = compute_load_by_period_month(appliances)
    baseline_kwh = sum(loads.values())
    baseline_cost = compute_cost(loads, prices)

    # Solaire appliqué principalement sur la période midday (12h-18h)
    solar_kwh_month = solar_production_month(solar_kwp, psh_midday, pr)
    midday_grid_after = max(0.0, loads["midday"] - solar_kwh_month)
    # Solaire auto-consommé = min(load_midday, solar_prod)
    solar_self = min(loads["midday"], solar_kwh_month)
    solar_excess = max(0.0, solar_kwh_month - loads["midday"])

    loads_after = dict(loads)
    loads_after["midday"] = midday_grid_after
    after_cost = compute_cost(loads_after, prices)
    after_kwh = sum(loads_after.values())

    savings_month = baseline_cost - after_cost
    savings_year = savings_month * 12.0

    payback_years = None
    if solar_cost > 0 and savings_year > 0:
        payback_years = solar_cost / savings_year

    # Gains nets sur 3 et 5 ans (sans maintenance/ inflation pour simplifier)
    net_3y = savings_year * 3.0 - solar_cost
    net_5y = savings_year * 5.0 - solar_cost

    # Dimensionnement recommandé : couvrir la charge midday
    recommended_kwp = 0.0
    if psh_midday > 0 and pr > 0:
        # Cible: solar_prod_month ≈ loads_midday => kWp ≈ load_midday / (PSH*PR*30)
        recommended_kwp = loads["midday"] / (psh_midday * pr * 30.0)

    return {
        "baseline": {
            "kwh_month": round(baseline_kwh, 2),
            "cost_month": round(baseline_cost, 2),
            "kwh_by_period_month": {k: round(v, 2) for k, v in loads.items()},
        },
        "solar": {
            "system_kwp": solar_kwp,
            "install_cost": solar_cost,
            "peak_sun_hours_midday": psh_midday,
            "performance_ratio": pr,
            "production_kwh_month": round(solar_kwh_month, 2),
            "self_consumed_kwh_month": round(solar_self, 2),
            "excess_kwh_month": round(solar_excess, 2),
            "recommended_system_kwp": round(recommended_kwp, 2),
        },
        "after": {
            "kwh_month": round(after_kwh, 2),
            "cost_month": round(after_cost, 2),
            "kwh_by_period_month": {k: round(v, 2) for k, v in loads_after.items()},
        },
        "savings": {
            "cost_savings_month": round(savings_month, 2),
            "cost_savings_year": round(savings_year, 2),
            "payback_years": None if payback_years is None else round(payback_years, 2),
            "net_savings_3y": round(net_3y, 2),
            "net_savings_5y": round(net_5y, 2),
        },
        "formulas": {
            "kwh_appliance": "kWh = (Puissance(W) × Heures × Quantité) / 1000",
            "month_factor": "kWh_mois ≈ kWh_jour × (4.345 × jours_par_semaine)",
            "solar_month": "Prod_solaire_mois ≈ kWp × PSH × PR × 30",
            "payback": "Temps_rentabilité (années) = Coût_installation / Économies_annuelles",
        }
    }
