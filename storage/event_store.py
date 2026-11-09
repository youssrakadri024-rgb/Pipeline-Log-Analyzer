"""Module STORAGE : enregistrement et lecture des tentatives de connexion.

Format d'une ligne du fichier data/events.log :
2026-11-09 12:30:01|LOGIN|user=alice|country=Maroc|status=SUCCESS|reason=-
"""
import os
from datetime import datetime

import config
from app_logger import get_logger

log = get_logger("storage")


def format_event(username, country, success, reason):
    """Construit la ligne de log d'une tentative de connexion."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    return "%s|LOGIN|user=%s|country=%s|status=%s|reason=%s" % (
        now, username, country, status, reason or "-"
    )


class EventStore:
    def __init__(self, path=None):
        self.path = path or config.EVENTS_FILE

    def append(self, line):
        """Ajoute une ligne. Retourne True si l'écriture a réussi."""
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            log.debug("Ligne enregistrée : %s", line)
            return True
        except PermissionError:
            log.error("Permission refusée pour écrire dans %s", self.path)
        except OSError as exc:
            log.error("Erreur d'écriture dans %s : %s", self.path, exc)
        return False

    def read_lines(self):
        """Retourne la liste des lignes (liste vide si le fichier n'existe pas encore)."""
        try:
            with open(self.path, "r", encoding="utf-8", errors="replace") as f:
                return [line.rstrip("\r\n") for line in f]
        except FileNotFoundError:
            log.info("Fichier %s inexistant : aucune tentative enregistrée", self.path)
        except PermissionError:
            log.error("Permission refusée pour lire %s", self.path)
        except OSError as exc:
            log.error("Erreur de lecture de %s : %s", self.path, exc)
        return []
