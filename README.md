# Agent Météo

Programme Python qui envoie chaque soir sur Discord la météo du lendemain : conditions,
températures minimale et maximale, risque de pluie et vent.

Les données viennent d'[Open-Meteo](https://open-meteo.com/) (gratuit, sans clé d'API) et
le message est envoyé via un webhook Discord.

## Installation

Python 3.10 ou plus est nécessaire.

```bash
pip install -r requirements.txt
```

## Configuration

1. Créer un webhook Discord : paramètres du salon > Intégrations > Webhooks > Nouveau webhook,
   puis copier l'URL.
2. Copier `.env.example` en `.env` et renseigner :

| Variable              | Description                              | Défaut   |
|-----------------------|------------------------------------------|----------|
| `DISCORD_WEBHOOK_URL` | URL du webhook Discord                   | -        |
| `VILLE`               | Ville dont on veut la météo              | `Troyes` |
| `HEURE_ENVOI`         | Heure d'envoi quotidienne (`HH:MM`)      | `20:00`  |

L'URL du webhook est secrète : le fichier `.env` n'est pas versionné.

## Utilisation

```bash
python main.py --apercu       # affiche le message sans l'envoyer
python main.py --maintenant   # envoie le message tout de suite, puis s'arrête
python main.py                # reste actif et envoie le message chaque jour à HEURE_ENVOI
```

Le mode sans option nécessite que le programme reste lancé et que l'ordinateur soit allumé.
Pour ne rien laisser ouvert, planifier `python main.py --maintenant` avec le Planificateur de
tâches Windows ou `cron`, en le lançant depuis le dossier du projet.

## Structure

```
main.py              point d'entrée et planification
src/config.py        lecture du fichier .env
src/meteo.py         appels à l'API météo et mise en forme du message
src/discord_notif.py envoi du message via le webhook
```
