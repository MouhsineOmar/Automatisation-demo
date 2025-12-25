"""Crée un profil + appareils démo + solaire démo."""
try:
    from .app import create_app  # type: ignore
    from .database import db  # type: ignore
    from .models import Profile, Appliance, SolarConfig  # type: ignore
except ImportError:
    from app import create_app  # type: ignore
    from database import db  # type: ignore
    from models import Profile, Appliance, SolarConfig  # type: ignore

def main():
    app = create_app()
    with app.app_context():
        db.create_all()

        p = Profile(
            name="Demo House",
            location_type="village",
            region="Example Region",
            currency="EUR",
            price_morning=0.22,
            price_midday=0.22,
            price_evening=0.25,
            price_night=0.18,
        )
        db.session.add(p)
        db.session.commit()

        # Lampes: 8 lampes de 60W utilisées le soir 5h/jour
        db.session.add(Appliance(
            profile_id=p.id, name="Lampes maison", category="lamp",
            power_watts=60, quantity=8, h_evening=5, days_per_week=7
        ))

        # Clim: 1200W, 1 unité, matin 2h + midi 4h + soir 2h
        db.session.add(Appliance(
            profile_id=p.id, name="Climatiseur", category="ac",
            power_watts=1200, quantity=1, h_morning=2, h_midday=4, h_evening=2, days_per_week=7
        ))

        # Frigo: 150W, 24h (approx)
        db.session.add(Appliance(
            profile_id=p.id, name="Réfrigérateur", category="fridge",
            power_watts=150, quantity=1, h_morning=6, h_midday=6, h_evening=6, h_night=6, days_per_week=7
        ))

        # Solaire: 3 kWp, coût 4500€, PSH 4.5, PR 0.75
        solar = SolarConfig(
            profile_id=p.id, system_size_kwp=3.0, install_cost=4500,
            peak_sun_hours_midday=4.5, performance_ratio=0.75
        )
        db.session.add(solar)
        db.session.commit()

        print(f"Demo profile created with id={p.id}")

if __name__ == "__main__":
    main()
