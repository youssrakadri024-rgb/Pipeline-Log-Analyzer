"""Module de journalisation de l'application.

Chaque module du projet appelle get_logger("nom_du_module") et obtient son
propre fichier : logs/<nom_du_module>.log. Les erreurs de chaque module sont
donc enregistrées séparément (consigne : logs par module).
"""
import logging
import os
import sys

from config import LOG_DIR

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(module_name):
    """Retourne un logger dédié au module, écrivant dans logs/<module>.log."""
    logger = logging.getLogger(module_name)
    if logger.handlers:  # évite les doublons si appelé plusieurs fois
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    formatter = logging.Formatter(LOG_FORMAT)

    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(LOG_DIR, module_name + ".log"), encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as exc:
        # Impossible d'écrire les logs : on prévient sur la sortie d'erreur
        print("ATTENTION: logs fichier indisponibles (%s)" % exc, file=sys.stderr)

    # Seules les vraies erreurs s'affichent dans le terminal (le reste va au fichier)
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.ERROR)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger
