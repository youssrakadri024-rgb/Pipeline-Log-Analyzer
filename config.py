"""Configuration centrale du projet Pipeline Log Analyzer."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Fichier où chaque tentative de connexion est enregistrée (une ligne par tentative)
EVENTS_FILE = os.path.join(DATA_DIR, "events.log")
# Page du dashboard générée par le programme
DASHBOARD_FILE = os.path.join(BASE_DIR, "serving", "dashboard.html")

# Comptes fictifs de démonstration
USERS = {
    "alice": "demo123",
    "bob": "demo123",
    "charlie": "demo123",
}
