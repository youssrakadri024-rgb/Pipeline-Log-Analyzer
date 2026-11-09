import os
import tempfile
import unittest

from log_analysis.log_parser import LogParser
from processing.authentication import Authenticator
from processing.login_service import LoginService
from processing.statistics import StatisticsCalculator
from serving.dashboard import Dashboard, escape_html
from storage.event_store import EventStore


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.store = EventStore(os.path.join(self.tmp, "events.log"))
        self.service = LoginService(store=self.store)

    def run_scenario(self):
        for u, p, c in [("alice", "demo123", "maroc"), ("bob", "faux123", "france"),
                        ("inconnu", "123", "maroc"), ("charlie", "demo123", "espagne")]:
            self.service.attempt(u, p, c)
        events, invalid = LogParser().parse_lines(self.store.read_lines())
        return StatisticsCalculator().compute(events), invalid

    def test_auth(self):
        a = Authenticator()
        self.assertEqual(a.authenticate("alice", "demo123"), (True, None))
        self.assertEqual(a.authenticate("alice", "x"), (False, "WRONG_PASSWORD"))
        self.assertEqual(a.authenticate("zzz", "x"), (False, "INVALID_USER"))

    def test_statistics(self):
        s, invalid = self.run_scenario()
        self.assertEqual(invalid, 0)
        self.assertEqual((s["total"], s["success"], s["failed"]), (4, 2, 2))
        self.assertEqual(s["failed_by_country"], [("France", 1), ("Maroc", 1)])
        self.assertEqual(s["success_by_user"], [("alice", 1), ("charlie", 1)])
        self.assertEqual(s["invalid_user_total"], 1)
        self.assertEqual(s["invalid_users"], [("inconnu", 1)])

    def test_bad_input_rejected(self):
        with self.assertRaises(ValueError):
            self.service.attempt("", "x", "Maroc")
        with self.assertRaises(ValueError):
            self.service.attempt("alice", "demo123", "123")
        with self.assertRaises(ValueError):
            self.service.attempt("alice", "demo123", "")
        self.assertEqual(self.store.read_lines(), [])

    def test_pipe_injection_cleaned(self):
        self.service.attempt("a|b\nc", "x", "Maroc")
        lines = self.store.read_lines()
        self.assertEqual(len(lines), 1)
        events, invalid = LogParser().parse_lines(lines)
        self.assertEqual((len(events), invalid), (1, 0))
        self.assertEqual(events[0]["user"], "a b c")

    def test_parser_invalid_and_blank_lines(self):
        good = "2026-11-09 12:00:00|LOGIN|user=alice|country=Maroc|status=SUCCESS|reason=-"
        events, invalid = LogParser().parse_lines([good, "", "n'importe quoi", good[:-3]])
        self.assertEqual((len(events), invalid), (1, 2))

    def test_parser_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            LogParser().parse_file(os.path.join(self.tmp, "absent.log"))

    def test_read_missing_store(self):
        self.assertEqual(EventStore(os.path.join(self.tmp, "x", "y.log")).read_lines(), [])

    def test_write_failure_returns_false(self):
        blocker = os.path.join(self.tmp, "fichier")
        open(blocker, "w").close()
        self.assertFalse(EventStore(os.path.join(blocker, "events.log")).append("x"))

    def test_html_dashboard(self):
        s, _ = self.run_scenario()
        d = Dashboard(os.path.join(self.tmp, "d.html"))
        self.assertTrue(d.write_html(s))
        with open(d.html_path, encoding="utf-8") as f:
            html = f.read()
        for expected in ("France", "Maroc", "alice", "charlie", "inconnu"):
            self.assertIn(expected, html)
        self.assertEqual(escape_html("<script>"), "&lt;script&gt;")

    def test_terminal_empty(self):
        text = Dashboard().terminal_text(StatisticsCalculator().compute([]))
        self.assertIn("Aucun échec", text)
        self.assertIn("Aucune connexion réussie", text)


if __name__ == "__main__":
    unittest.main()