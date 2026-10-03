"""Envoi d'un message sur Discord grâce à un webhook."""

import requests


def envoyer_message(webhook_url, texte):
    """Poste `texte` dans le salon Discord lié au webhook."""
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL est vide : vérifie ton fichier .env")

    reponse = requests.post(webhook_url, json={"content": texte}, timeout=10)
    reponse.raise_for_status()  # lève une erreur si Discord répond 4xx / 5xx
