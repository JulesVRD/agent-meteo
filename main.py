"""Point d'entrée : envoie chaque soir la météo du lendemain sur Discord.

Utilisation :
    python main.py                # tourne en continu et envoie à l'heure prévue
    python main.py --maintenant   # envoie un message tout de suite puis s'arrête
    python main.py --apercu       # affiche le message sans l'envoyer sur Discord
"""

import argparse
import time

import schedule

from src import config
from src.discord_notif import envoyer_message
from src.meteo import formater_message, recuperer_meteo_demain, trouver_ville


def envoyer_meteo(apercu=False):
    """Récupère la météo de demain et l'envoie (ou l'affiche si apercu=True)."""
    try:
        nom_ville, latitude, longitude = trouver_ville(config.VILLE)
        meteo = recuperer_meteo_demain(latitude, longitude)
        message = formater_message(nom_ville, meteo)

        if apercu:
            print(message)
        else:
            envoyer_message(config.WEBHOOK_URL, message)
            print("Message envoyé sur Discord.")
    except Exception as erreur:
        # On affiche l'erreur sans arrêter le programme :
        # il réessaiera demain soir.
        print(f"Erreur : {erreur}")


def main():
    parser = argparse.ArgumentParser(description="Météo de demain sur Discord")
    parser.add_argument("--maintenant", action="store_true", help="envoie un message tout de suite")
    parser.add_argument("--apercu", action="store_true", help="affiche le message sans l'envoyer")
    args = parser.parse_args()

    # Mode "une seule fois" : utile pour tester ou pour le planificateur de Windows
    if args.maintenant or args.apercu:
        envoyer_meteo(apercu=args.apercu)
        return

    # Mode "tourne en continu" : on planifie l'envoi chaque jour
    schedule.every().day.at(config.HEURE_ENVOI).do(envoyer_meteo)
    print(f"Programme lancé : envoi tous les jours à {config.HEURE_ENVOI} (Ctrl+C pour arrêter).")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
