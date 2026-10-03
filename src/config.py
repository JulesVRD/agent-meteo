"""Configuration du programme : lit les valeurs du fichier .env."""

import os

from dotenv import load_dotenv

# Charge les variables du fichier .env dans l'environnement
load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
VILLE = os.getenv("VILLE", "Troyes")
HEURE_ENVOI = os.getenv("HEURE_ENVOI", "20:00")
