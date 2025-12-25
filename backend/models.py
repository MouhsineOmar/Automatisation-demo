from datetime import datetime
# Support exécution package (python -m backend.app) ET script (python app.py)
try:
    from .database import db  # type: ignore
except ImportError:
    from database import db  # type: ignore

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_type = db.Column(db.String(40), nullable=False)  # countryside | village | city
    region = db.Column(db.String(120), nullable=True)  # ville/pays/zone
    currency = db.Column(db.String(10), default="EUR")

    # Tarifs par période (prix du kWh)
    price_morning = db.Column(db.Float, nullable=False, default=0.20)
    price_midday  = db.Column(db.Float, nullable=False, default=0.20)
    price_evening = db.Column(db.Float, nullable=False, default=0.20)
    price_night   = db.Column(db.Float, nullable=False, default=0.20)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appliances = db.relationship("Appliance", backref="profile", cascade="all, delete-orphan")
    solar = db.relationship("SolarConfig", backref="profile", uselist=False, cascade="all, delete-orphan")

class Appliance(db.Model):
    __tablename__ = "appliances"
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)

    name = db.Column(db.String(120), nullable=False)         # ex: Lampes salon, Clim chambre
    category = db.Column(db.String(60), nullable=False)      # lamp | ac | fridge | tv | ...
    power_watts = db.Column(db.Float, nullable=False)        # W
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Heures d'utilisation par jour et par période (morning/midday/evening/night)
    h_morning = db.Column(db.Float, nullable=False, default=0.0)
    h_midday  = db.Column(db.Float, nullable=False, default=0.0)
    h_evening = db.Column(db.Float, nullable=False, default=0.0)
    h_night   = db.Column(db.Float, nullable=False, default=0.0)

    days_per_week = db.Column(db.Integer, nullable=False, default=7)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SolarConfig(db.Model):
    __tablename__ = "solar_configs"
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, unique=True)

    system_size_kwp = db.Column(db.Float, nullable=False, default=0.0)  # kWp
    install_cost = db.Column(db.Float, nullable=False, default=0.0)     # monnaie du profil
    performance_ratio = db.Column(db.Float, nullable=False, default=0.75)  # pertes (0.70-0.85)
    peak_sun_hours_midday = db.Column(db.Float, nullable=False, default=4.0)  # heures solaires utiles /jour

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
