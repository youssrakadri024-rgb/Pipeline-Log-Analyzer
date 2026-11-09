"""Module PROCESSING : validation de la saisie + authentification + enregistrement."""
import re

from app_logger import get_logger
from processing.authentication import Authenticator
from storage.event_store import EventStore, format_event

log = get_logger("login_service")

COUNTRY_PATTERN = re.compile(r"^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ \-']*$")


def clean(text):
    """Supprime les caractères qui casseraient le format du fichier de log."""
    text = (text or "").replace("|", " ").replace("\r", " ").replace("\n", " ")
    return " ".join(text.split())


class LoginService:
    def __init__(self, authenticator=None, store=None):
        self.authenticator = authenticator or Authenticator()
        self.store = store or EventStore()

    def attempt(self, username, password, country):
        """Retourne (succes, raison). Lève ValueError si la saisie est invalide."""
        username = clean(username)
        country = clean(country)
        if not username:
            log.warning("Saisie refusée : nom d'utilisateur vide")
            raise ValueError("Le nom d'utilisateur ne peut pas être vide.")
        if not COUNTRY_PATTERN.match(country):
            log.warning("Saisie refusée : pays invalide %r", country)
            raise ValueError("Pays invalide : utilise des lettres (ex. Maroc, France).")
        country = country.title()

        success, reason = self.authenticator.authenticate(username, password or "")
        saved = self.store.append(format_event(username, country, success, reason))
        if not saved:
            log.error("Tentative de %s non enregistrée (échec d'écriture)", username)
            raise OSError("La tentative n'a pas pu être enregistrée (voir logs/storage.log).")
        if success:
            log.info("Connexion réussie | user=%s | pays=%s", username, country)
        else:
            log.warning("Connexion échouée | user=%s | pays=%s | raison=%s",
                        username, country, reason)
        return success, reason
