from flask import Flask, jsonify, request
from flask_cors import CORS

# Imports conditionnels (package vs script)
try:
    from .config import Config  # type: ignore
    from .database import db  # type: ignore
    from .models import Profile, Appliance, SolarConfig  # type: ignore
    from .services.analysis import analyze, ApplianceInput  # type: ignore
    from .services.recommendations import recommend  # type: ignore
except ImportError:
    from config import Config  # type: ignore
    from database import db  # type: ignore
    from models import Profile, Appliance, SolarConfig  # type: ignore
    from services.analysis import analyze, ApplianceInput  # type: ignore
    from services.recommendations import recommend  # type: ignore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ---- Profiles ----
    @app.post("/api/profiles")
    def create_profile():
        payload = request.json or {}
        p = Profile(
            name=payload.get("name", "My Home"),
            location_type=payload.get("location_type", "city"),
            region=payload.get("region"),
            currency=payload.get("currency", "EUR"),
            price_morning=float(payload.get("price_morning", 0.20)),
            price_midday=float(payload.get("price_midday", 0.20)),
            price_evening=float(payload.get("price_evening", 0.20)),
            price_night=float(payload.get("price_night", 0.20)),
        )
        db.session.add(p)
        db.session.commit()
        return jsonify({"id": p.id})

    @app.get("/api/profiles")
    def list_profiles():
        profiles = Profile.query.order_by(Profile.created_at.desc()).all()
        return jsonify([{
            "id": p.id,
            "name": p.name,
            "location_type": p.location_type,
            "region": p.region,
            "currency": p.currency,
            "prices": {
                "morning": p.price_morning, "midday": p.price_midday,
                "evening": p.price_evening, "night": p.price_night
            }
        } for p in profiles])

    @app.get("/api/profiles/<int:profile_id>")
    def get_profile(profile_id: int):
        p = Profile.query.get_or_404(profile_id)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "location_type": p.location_type,
            "region": p.region,
            "currency": p.currency,
            "prices": {
                "morning": p.price_morning, "midday": p.price_midday,
                "evening": p.price_evening, "night": p.price_night
            }
        })

    # ---- Appliances ----
    @app.post("/api/profiles/<int:profile_id>/appliances")
    def add_appliance(profile_id: int):
        Profile.query.get_or_404(profile_id)
        payload = request.json or {}
        a = Appliance(
            profile_id=profile_id,
            name=payload["name"],
            category=payload["category"],
            power_watts=float(payload["power_watts"]),
            quantity=int(payload.get("quantity", 1)),
            h_morning=float(payload.get("h_morning", 0)),
            h_midday=float(payload.get("h_midday", 0)),
            h_evening=float(payload.get("h_evening", 0)),
            h_night=float(payload.get("h_night", 0)),
            days_per_week=int(payload.get("days_per_week", 7)),
        )
        db.session.add(a)
        db.session.commit()
        return jsonify({"id": a.id})

    @app.get("/api/profiles/<int:profile_id>/appliances")
    def list_appliances(profile_id: int):
        Profile.query.get_or_404(profile_id)
        items = Appliance.query.filter_by(profile_id=profile_id).all()
        return jsonify([{
            "id": a.id, "name": a.name, "category": a.category,
            "power_watts": a.power_watts, "quantity": a.quantity,
            "h_morning": a.h_morning, "h_midday": a.h_midday,
            "h_evening": a.h_evening, "h_night": a.h_night,
            "days_per_week": a.days_per_week
        } for a in items])

    # ---- Solar ----
    @app.post("/api/profiles/<int:profile_id>/solar")
    def set_solar(profile_id: int):
        p = Profile.query.get_or_404(profile_id)
        payload = request.json or {}
        solar = SolarConfig.query.filter_by(profile_id=profile_id).first()
        if solar is None:
            solar = SolarConfig(profile_id=profile_id)
            db.session.add(solar)
        solar.system_size_kwp = float(payload.get("system_size_kwp", solar.system_size_kwp or 0))
        solar.install_cost = float(payload.get("install_cost", solar.install_cost or 0))
        solar.performance_ratio = float(payload.get("performance_ratio", solar.performance_ratio or 0.75))
        solar.peak_sun_hours_midday = float(payload.get("peak_sun_hours_midday", solar.peak_sun_hours_midday or 4.0))
        db.session.commit()
        return jsonify({"ok": True})

    @app.get("/api/profiles/<int:profile_id>/solar")
    def get_solar(profile_id: int):
        Profile.query.get_or_404(profile_id)
        solar = SolarConfig.query.filter_by(profile_id=profile_id).first()
        if solar is None:
            return jsonify(None)
        return jsonify({
            "system_size_kwp": solar.system_size_kwp,
            "install_cost": solar.install_cost,
            "performance_ratio": solar.performance_ratio,
            "peak_sun_hours_midday": solar.peak_sun_hours_midday,
        })

    # ---- Analysis ----
    @app.get("/api/profiles/<int:profile_id>/analysis")
    def run_analysis(profile_id: int):
        p = Profile.query.get_or_404(profile_id)
        aps = Appliance.query.filter_by(profile_id=profile_id).all()
        appliances = [
            ApplianceInput(
                name=a.name, category=a.category, power_watts=a.power_watts, quantity=a.quantity,
                h_morning=a.h_morning, h_midday=a.h_midday, h_evening=a.h_evening, h_night=a.h_night,
                days_per_week=a.days_per_week
            )
            for a in aps
        ]
        prices = {
            "morning": p.price_morning,
            "midday": p.price_midday,
            "evening": p.price_evening,
            "night": p.price_night,
        }
        solar = SolarConfig.query.filter_by(profile_id=profile_id).first()
        solar_kwp = solar.system_size_kwp if solar else 0.0
        solar_cost = solar.install_cost if solar else 0.0
        psh = solar.peak_sun_hours_midday if solar else 4.0
        pr = solar.performance_ratio if solar else 0.75

        result = analyze(
            appliances=appliances,
            prices=prices,
            solar_kwp=solar_kwp,
            solar_cost=solar_cost,
            psh_midday=psh,
            pr=pr,
        )
        result["recommendations"] = recommend(p.location_type, appliances, has_solar=bool(solar_kwp and solar_kwp > 0))
        result["currency"] = p.currency
        result["profile"] = {
            "id": p.id,
            "name": p.name,
            "location_type": p.location_type,
            "region": p.region,
        }
        return jsonify(result)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
