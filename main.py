"""Pipeline Log Analyzer — programme principal (menu interactif)."""
from app_logger import get_logger
from log_analysis.log_parser import LogParser
from processing.login_service import LoginService
from processing.statistics import StatisticsCalculator
from serving.dashboard import Dashboard
from storage.event_store import EventStore

log = get_logger("main")

MENU = """
====================================
       PIPELINE LOG ANALYZER
====================================

1. Tester une connexion
2. Afficher le dashboard (terminal + Opera)
3. Analyser un autre fichier de log
4. Quitter
"""

REASON_LABELS = {
    "INVALID_USER": "utilisateur invalide",
    "WRONG_PASSWORD": "mot de passe incorrect",
}


class Application:
    def __init__(self):
        self.store = EventStore()
        self.parser = LogParser()
        self.calculator = StatisticsCalculator()
        self.dashboard = Dashboard()
        self.login_service = LoginService(store=self.store)
        self.browser_opened = False

    def current_stats(self):
        events, _invalid = self.parser.parse_lines(self.store.read_lines())
        return self.calculator.compute(events)

    def refresh_html(self):
        """Régénère la page HTML (appelé après chaque tentative)."""
        return self.dashboard.write_html(self.current_stats())

    def action_test_login(self):
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        country = input("Pays : ")
        try:
            success, reason = self.login_service.attempt(username, password, country)
        except ValueError as exc:
            print("\n[SAISIE REFUSÉE] %s" % exc)
            return
        except OSError as exc:
            print("\n[ERREUR] %s" % exc)
            return
        if success:
            print("\n[OK] Connexion réussie : bienvenue %s !" % username.strip())
        else:
            print("\n[ECHEC] Connexion échouée : %s." % REASON_LABELS.get(reason, reason))
        self.refresh_html()  # le dashboard HTML se met à jour après chaque tentative

    def action_dashboard(self):
        stats = self.current_stats()
        print(self.dashboard.terminal_text(stats))
        if not self.dashboard.write_html(stats):
            print("\nImpossible d'écrire la page HTML (voir logs/serving.log).")
            return
        if not self.browser_opened:
            self.browser_opened = self.dashboard.open_in_browser()
        if self.browser_opened:
            print("\nDashboard ouvert dans le navigateur (mise à jour toutes les 3 s).")
        else:
            print("\nOuvre ce fichier dans Opera (glisse-le dans la fenêtre) :")
            print(self.dashboard.html_path)

    def action_analyze_file(self):
        path = input("Chemin du fichier de log : ").strip().strip('"')
        if not path:
            print("Aucun chemin saisi.")
            return
        try:
            events, invalid = self.parser.parse_file(path)
        except FileNotFoundError:
            print("Fichier introuvable : %s" % path)
            return
        except OSError as exc:
            print("Impossible de lire le fichier : %s" % exc)
            return
        print("\n%d lignes valides, %d lignes invalides ignorées." % (len(events), invalid))
        print(self.dashboard.terminal_text(self.calculator.compute(events)))

    def run(self):
        log.info("Programme démarré")
        actions = {
            "1": self.action_test_login,
            "2": self.action_dashboard,
            "3": self.action_analyze_file,
        }
        try:
            while True:
                print(MENU)
                choice = input("Votre choix : ").strip()
                if choice == "4":
                    break
                action = actions.get(choice)
                if action is None:
                    print("Choix invalide, tape 1, 2, 3 ou 4.")
                    continue
                try:
                    action()
                except Exception as exc:  # aucune erreur ne doit fermer le programme
                    log.exception("Erreur inattendue dans l'action %s : %s", choice, exc)
                    print("Une erreur inattendue est survenue (voir logs/main.log).")
        except (KeyboardInterrupt, EOFError):
            print()
        finally:
            log.info("Programme arrêté")
            print("Fin du programme.")


if __name__ == "__main__":
    Application().run()
