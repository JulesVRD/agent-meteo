"""Récupération et mise en forme de la météo avec l'API gratuite Open-Meteo."""

from datetime import date

import requests

URL_GEOCODAGE = "https://geocoding-api.open-meteo.com/v1/search"
URL_PREVISIONS = "https://api.open-meteo.com/v1/forecast"

# Codes météo WMO renvoyés par l'API -> (description, emoji)
CODES_METEO = {
    0: ("Ciel dégagé", "☀️"),
    1: ("Plutôt dégagé", "🌤️"),
    2: ("Partiellement nuageux", "⛅"),
    3: ("Couvert", "☁️"),
    45: ("Brouillard", "🌫️"),
    48: ("Brouillard givrant", "🌫️"),
    51: ("Bruine légère", "🌦️"),
    53: ("Bruine", "🌦️"),
    55: ("Bruine dense", "🌦️"),
    56: ("Bruine verglaçante", "🌧️"),
    57: ("Bruine verglaçante forte", "🌧️"),
    61: ("Pluie faible", "🌧️"),
    63: ("Pluie modérée", "🌧️"),
    65: ("Pluie forte", "🌧️"),
    66: ("Pluie verglaçante", "🌧️"),
    67: ("Pluie verglaçante forte", "🌧️"),
    71: ("Neige faible", "❄️"),
    73: ("Neige modérée", "❄️"),
    75: ("Neige forte", "❄️"),
    77: ("Grains de neige", "❄️"),
    80: ("Averses faibles", "🌦️"),
    81: ("Averses", "🌦️"),
    82: ("Averses violentes", "⛈️"),
    85: ("Averses de neige", "❄️"),
    86: ("Fortes averses de neige", "❄️"),
    95: ("Orage", "⛈️"),
    96: ("Orage avec grêle", "⛈️"),
    99: ("Orage violent avec grêle", "⛈️"),
}

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def trouver_ville(nom):
    """Cherche une ville par son nom. Renvoie (nom, latitude, longitude)."""
    reponse = requests.get(
        URL_GEOCODAGE,
        params={"name": nom, "count": 1, "language": "fr"},
        timeout=10,
    )
    reponse.raise_for_status()

    resultats = reponse.json().get("results")
    if not resultats:
        raise ValueError(f"Ville introuvable : {nom}")

    ville = resultats[0]
    return ville["name"], ville["latitude"], ville["longitude"]


def recuperer_meteo_demain(latitude, longitude):
    """Renvoie un dictionnaire avec les prévisions de demain."""
    reponse = requests.get(
        URL_PREVISIONS,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "weather_code,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max,precipitation_sum,wind_speed_10m_max"
            ),
            "timezone": "Europe/Paris",
            "forecast_days": 2,  # aujourd'hui + demain
        },
        timeout=10,
    )
    reponse.raise_for_status()
    jour = reponse.json()["daily"]

    # Dans les listes renvoyées, l'indice 0 = aujourd'hui et l'indice 1 = demain
    return {
        "date": jour["time"][1],
        "code": jour["weather_code"][1],
        "temp_max": jour["temperature_2m_max"][1],
        "temp_min": jour["temperature_2m_min"][1],
        "proba_pluie": jour["precipitation_probability_max"][1],
        "pluie_mm": jour["precipitation_sum"][1],
        "vent_max": jour["wind_speed_10m_max"][1],
    }


def formater_date(date_iso):
    """'2026-10-04' -> 'dimanche 4 octobre'."""
    d = date.fromisoformat(date_iso)
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}"


def conseils(meteo):
    """Petits conseils selon la météo (liste de phrases, éventuellement vide)."""
    liste = []
    if meteo["proba_pluie"] >= 50:
        liste.append("☔ Prends un parapluie !")
    if meteo["temp_min"] <= 0:
        liste.append("🧊 Risque de gel, couvre-toi bien.")
    if meteo["temp_max"] >= 30:
        liste.append("🥵 Grosse chaleur, pense à bien t'hydrater.")
    if meteo["vent_max"] >= 50:
        liste.append("💨 Vent fort prévu, attention dehors.")
    return liste


def formater_message(ville, meteo):
    """Construit le texte envoyé sur Discord."""
    description, emoji = CODES_METEO.get(meteo["code"], ("Météo inconnue", "❓"))

    lignes = [
        f"**Météo de demain à {ville}** - {formater_date(meteo['date'])}",
        f"{emoji} {description}",
        f"🌡️ Température : {meteo['temp_min']:.0f}°C à {meteo['temp_max']:.0f}°C",
        f"🌧️ Pluie : {meteo['proba_pluie']}% de risque ({meteo['pluie_mm']} mm)",
        f"💨 Vent : jusqu'à {meteo['vent_max']:.0f} km/h",
    ]

    lignes.extend(conseils(meteo))
    return "\n".join(lignes)
