"""Module d'analyse : calcule les 3 indicateurs demandés pour le dashboard."""
from collections import Counter

from app_logger import get_logger
from geo import country_of

logger = get_logger("analyzer")


def failed_by_country(events, networks):
    """Indicateur 1 : nombre de tentatives échouées par pays."""
    counter = Counter()
    for event in events:
        if event["status"] == "failed":
            counter[country_of(event["ip"], networks)] += 1
    return counter


def success_by_user(events):
    """Indicateur 2 : nombre de tentatives réussies par utilisateur."""
    counter = Counter()
    for event in events:
        if event["status"] == "success":
            counter[event["user"]] += 1
    return counter


def failed_invalid_user(events):
    """Indicateur 3 : tentatives échouées avec 'invalid user'.

    Retourne (total, compteur par nom d'utilisateur testé).
    """
    counter = Counter()
    for event in events:
        if event["status"] == "failed" and event["invalid_user"]:
            counter[event["user"]] += 1
    return sum(counter.values()), counter


def analyze(events, networks):
    """Calcule tous les indicateurs et retourne un dictionnaire."""
    if not events:
        logger.warning("Aucun événement à analyser")
    invalid_total, invalid_by_user = failed_invalid_user(events)
    result = {
        "failed_by_country": failed_by_country(events, networks),
        "success_by_user": success_by_user(events),
        "invalid_total": invalid_total,
        "invalid_by_user": invalid_by_user,
        "total_events": len(events),
    }
    logger.info("Analyse terminée sur %d événements", len(events))
    return result