"""Module SERVING : affichage du dashboard (terminal + page HTML ouverte dans Opera)."""
import os
from datetime import datetime

import config
from app_logger import get_logger

log = get_logger("serving")


def escape_html(text):
    """Remplace les caractères spéciaux HTML (évite d'injecter du code dans la page)."""
    text = str(text)
    for old, new in (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;")):
        text = text.replace(old, new)
    return text


class Dashboard:
    def __init__(self, html_path=None):
        self.html_path = html_path or config.DASHBOARD_FILE

    # ---------- terminal ----------
    def terminal_text(self, stats):
        line = "=" * 55
        out = ["", line, "             PIPELINE LOG ANALYZER", line,
               "Nombre total de tentatives enregistrées : %d" % stats["total"],
               "Réussies : %d   Échecs : %d   Taux de réussite : %s %%" % (
                   stats["success"], stats["failed"], stats["success_rate"]),
               "", "1. Tentatives échouées par pays"]
        if stats["failed_by_country"]:
            out += ["   %s : %d" % item for item in stats["failed_by_country"]]
        else:
            out.append("   Aucun échec.")
        out += ["", "2. Tentatives réussies par utilisateur"]
        if stats["success_by_user"]:
            out += ["   %s : %d" % item for item in stats["success_by_user"]]
        else:
            out.append("   Aucune connexion réussie.")
        out += ["", "3. Tentatives échouées avec un utilisateur invalide (invalid user)",
                "   Total : %d" % stats["invalid_user_total"]]
        out += ["   %s : %d" % item for item in stats["invalid_users"]]
        out.append(line)
        return "\n".join(out)

    # ---------- HTML ----------
    def _table(self, title, headers, rows, empty_text):
        html = ["<div class='card'><h2>%s</h2>" % escape_html(title)]
        if rows:
            html.append("<table><tr>%s</tr>" % "".join(
                "<th>%s</th>" % escape_html(h) for h in headers))
            for name, number in rows:
                html.append("<tr><td>%s</td><td>%d</td></tr>" % (escape_html(name), number))
            html.append("</table>")
        else:
            html.append("<p class='empty'>%s</p>" % escape_html(empty_text))
        html.append("</div>")
        return "".join(html)

    def html_text(self, stats):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        parts = [
            "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>",
            "<meta http-equiv='refresh' content='3'>",
            "<title>Pipeline Log Analyzer</title><style>",
            "body{font-family:Arial,sans-serif;background:#f4f6fb;margin:0;color:#1f2937}",
            "header{background:#1e3a8a;color:#fff;padding:18px 28px}",
            "header h1{margin:0;font-size:22px}header p{margin:4px 0 0;font-size:13px;opacity:.8}",
            "main{max-width:1000px;margin:auto;padding:22px}",
            ".cards{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:18px}",
            ".stat{flex:1;min-width:170px;background:#fff;border-radius:10px;padding:16px;border:1px solid #e5e7eb}",
            ".stat b{display:block;font-size:34px}.stat span{color:#6b7280}",
            ".blue b{color:#2563eb}.green b{color:#16a34a}.red b{color:#dc2626}",
            ".card{background:#fff;border-radius:10px;padding:16px;margin-bottom:16px;border:1px solid #e5e7eb}",
            "h2{font-size:16px;margin:0 0 10px}table{width:100%;border-collapse:collapse}",
            "th,td{text-align:left;padding:8px;border-bottom:1px solid #e5e7eb}",
            ".empty{color:#6b7280;font-style:italic}",
            "</style></head><body>",
            "<header><h1>Pipeline Log Analyzer</h1>",
            "<p>Mise à jour automatique toutes les 3 s &middot; généré le %s</p></header><main>" % now,
            "<div class='cards'>",
            "<div class='stat blue'><b>%d</b><span>Total tentatives</span></div>" % stats["total"],
            "<div class='stat green'><b>%d</b><span>Réussites</span></div>" % stats["success"],
            "<div class='stat red'><b>%d</b><span>Échecs</span></div>" % stats["failed"],
            "</div>",
            self._table("Tentatives échouées par pays", ["Pays", "Nombre"],
                        stats["failed_by_country"], "Aucun échec."),
            self._table("Tentatives réussies par utilisateur", ["Utilisateur", "Nombre"],
                        stats["success_by_user"], "Aucune connexion réussie."),
            self._table("Tentatives échouées avec un utilisateur invalide (total : %d)"
                        % stats["invalid_user_total"], ["Utilisateur invalide", "Nombre"],
                        stats["invalid_users"], "Aucune tentative avec un utilisateur invalide."),
            "</main></body></html>",
        ]
        return "".join(parts)

    def write_html(self, stats):
        """Écrit dashboard.html. Retourne True si l'écriture a réussi."""
        try:
            os.makedirs(os.path.dirname(self.html_path), exist_ok=True)
            with open(self.html_path, "w", encoding="utf-8") as f:
                f.write(self.html_text(stats))
            return True
        except PermissionError:
            log.error("Permission refusée pour écrire %s", self.html_path)
        except OSError as exc:
            log.error("Erreur d'écriture de %s : %s", self.html_path, exc)
        return False

    def open_in_browser(self):
        """Ouvre la page avec le navigateur par défaut (Windows). Retourne True si réussi."""
        try:
            os.startfile(self.html_path)  # n'existe que sous Windows
            return True
        except AttributeError:
            log.warning("os.startfile indisponible sur ce système")
        except OSError as exc:
            log.error("Ouverture du navigateur impossible : %s", exc)
        return False
