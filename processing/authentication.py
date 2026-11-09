"""Module PROCESSING : vérification des identifiants."""
import config
from app_logger import get_logger

log = get_logger("authentication")

REASON_INVALID_USER = "INVALID_USER"
REASON_WRONG_PASSWORD = "WRONG_PASSWORD"


class Authenticator:
    def __init__(self, users=None):
        self.users = config.USERS if users is None else users

    def authenticate(self, username, password):
        """Retourne (succes, raison). La raison vaut None en cas de succès."""
        if username not in self.users:
            log.warning("Utilisateur inconnu : %s", username)
            return False, REASON_INVALID_USER
        if self.users[username] != password:
            log.warning("Mot de passe incorrect pour : %s", username)
            return False, REASON_WRONG_PASSWORD
        return True, None
