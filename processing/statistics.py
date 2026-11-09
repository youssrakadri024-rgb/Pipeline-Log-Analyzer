"""Module PROCESSING : calcul des statistiques demandées pour le dashboard."""
from app_logger import get_logger

log = get_logger("statistics")


def _sorted_items(counts):
    """Trie par nombre décroissant puis par nom."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


class StatisticsCalculator:
    def compute(self, events):
        failed_by_country = {}
        success_by_user = {}
        invalid_users = {}
        success = 0
        failed = 0

        for event in events:
            try:
                if event["status"] == "SUCCESS":
                    success += 1
                    user = event["user"]
                    success_by_user[user] = success_by_user.get(user, 0) + 1
                else:
                    failed += 1
                    country = event["country"]
                    failed_by_country[country] = failed_by_country.get(country, 0) + 1
                    if event["reason"] == "INVALID_USER":
                        user = event["user"]
                        invalid_users[user] = invalid_users.get(user, 0) + 1
            except KeyError as exc:
                log.error("Événement incomplet ignoré (champ manquant %s) : %s", exc, event)

        total = success + failed
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": round(100.0 * success / total, 1) if total else 0.0,
            "failed_by_country": _sorted_items(failed_by_country),
            "success_by_user": _sorted_items(success_by_user),
            "invalid_user_total": sum(invalid_users.values()),
            "invalid_users": _sorted_items(invalid_users),
        }
