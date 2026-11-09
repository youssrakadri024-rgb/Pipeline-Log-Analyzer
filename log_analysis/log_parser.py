"""Module LOG_ANALYSIS : lecture des lignes de log avec des expressions régulières (re)."""
import re

from app_logger import get_logger

log = get_logger("log_analysis")

LINE_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2})\|LOGIN\|"
    r"user=(?P<user>[^|]+)\|country=(?P<country>[^|]+)\|"
    r"status=(?P<status>SUCCESS|FAILED)\|reason=(?P<reason>[A-Z_-]+)$"
)


class LogParser:
    def parse_line(self, line):
        """Retourne un dict si la ligne est valide, sinon None."""
        match = LINE_PATTERN.match(line.strip())
        if match is None:
            return None
        return match.groupdict()

    def parse_lines(self, lines):
        """Retourne (liste d'événements, nombre de lignes invalides)."""
        events = []
        invalid = 0
        for number, line in enumerate(lines, start=1):
            if not line.strip():
                continue  # ligne vide : ignorée
            event = self.parse_line(line)
            if event is None:
                invalid += 1
                log.warning("Ligne %d invalide ignorée : %r", number, line[:80])
            else:
                events.append(event)
        return events, invalid

    def parse_file(self, path):
        """Lit un fichier de log. Lève FileNotFoundError / OSError (après les avoir journalisées)."""
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = [line.rstrip("\r\n") for line in f]
        except FileNotFoundError:
            log.error("Fichier de log introuvable : %s", path)
            raise
        except IsADirectoryError:
            log.error("Le chemin est un dossier, pas un fichier : %s", path)
            raise
        except PermissionError:
            log.error("Permission refusée pour lire : %s", path)
            raise
        except OSError as exc:
            log.error("Erreur de lecture de %s : %s", path, exc)
            raise
        events, invalid = self.parse_lines(lines)
        log.info("Fichier %s : %d événements valides, %d lignes invalides",
                 path, len(events), invalid)
        return events, invalid
