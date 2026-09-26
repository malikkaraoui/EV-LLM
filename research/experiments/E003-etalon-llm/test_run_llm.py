"""Tests hors ligne de run_llm.py (aucun appel reseau). python3 -m unittest -v test_run_llm"""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run_llm

BOOL_Q = {"type": "boolean", "instructions": "?"}
CHOICE_Q = {"type": "choice", "instructions": "?",
            "criteria": {"contradiction": "a", "coherent": "b", "indetermine": "c"}}


class ParseTest(unittest.TestCase):
    def test_strict_boolean(self):
        self.assertEqual(run_llm.parse_answer('{"reponse": true, "confiance": 0.9}', BOOL_Q),
                         (True, 0.9, None))

    def test_strict_choice_with_whitespace(self):
        rep, conf, why = run_llm.parse_answer(
            '\n {"reponse": "indetermine", "confiance": 1} \n', CHOICE_Q)
        self.assertEqual((rep, conf, why), ("indetermine", 1.0, None))

    def test_non_strict_rejected(self):
        bad = [
            '```json\n{"reponse": true, "confiance": 0.9}\n```',   # bloc de code
            'Réponse : {"reponse": true, "confiance": 0.9}',      # texte autour
            '{"reponse": true, "confiance": 0.9, "raison": "x"}',  # cle en trop
            '{"reponse": true}',                                  # cle manquante
            '{"reponse": "true", "confiance": 0.9}',              # chaine au lieu de booleen
            '{"reponse": true, "confiance": 1.2}',                # hors [0,1]
            '{"reponse": true, "confiance": true}',               # booleen comme confiance
            '{"reponse": true, "confiance": "0.9"}',              # chaine comme confiance
            '[true, 0.9]',
            '',
        ]
        for text in bad:
            with self.subTest(text=text):
                self.assertIsNotNone(run_llm.parse_answer(text, BOOL_Q)[2])
        self.assertIsNotNone(run_llm.parse_answer(None, BOOL_Q)[2])

    def test_choice_outside_options(self):
        self.assertIsNotNone(
            run_llm.parse_answer('{"reponse": "contradictoire", "confiance": 0.9}', CHOICE_Q)[2])
        self.assertIsNotNone(
            run_llm.parse_answer('{"reponse": true, "confiance": 0.9}', CHOICE_Q)[2])


class AggregateTest(unittest.TestCase):
    def test_conforme(self):
        r = run_llm.aggregate(True, [(True, 0.9), (True, 0.7), (True, 0.8)])
        self.assertEqual((r["obtenu"], r["p"], r["conforme"], r["faux_et_sur"]),
                         (True, 0.8, True, False))
        self.assertEqual(r["stabilite"], [0.7, 0.9])

    def test_faux_et_sur(self):
        r = run_llm.aggregate(False, [(True, 0.95), (True, 0.85), (False, 0.3)])
        self.assertEqual((r["obtenu"], r["p"], r["conforme"], r["faux_et_sur"]),
                         (True, 0.9, False, True))
        self.assertEqual(r["n_faux_et_sur_reps"], 2)

    def test_faux_pas_sur(self):
        r = run_llm.aggregate("indetermine", [("contradiction", 0.7)] * 3)
        self.assertEqual((r["conforme"], r["faux_et_sur"], r["n_faux_et_sur_reps"]),
                         (False, False, 0))

    def test_seuil_08_inclus(self):
        r = run_llm.aggregate(True, [(False, 0.8)])
        self.assertTrue(r["faux_et_sur"])

    def test_instable(self):
        r = run_llm.aggregate(True, [(True, 0.9), (False, 0.9)])
        self.assertEqual((r["obtenu"], r["conforme"], r["faux_et_sur"]),
                         ("INSTABLE", False, False))
        self.assertEqual(r["n_faux_et_sur_reps"], 1)

    def test_non_parse(self):
        r = run_llm.aggregate(True, [])
        self.assertEqual((r["obtenu"], r["conforme"], r["faux_et_sur"]),
                         ("NON_PARSE", None, None))


class SummarizeTest(unittest.TestCase):
    def test_rows_from_records(self):
        case = {"id": "C", "famille": "f", "state": "s", "questions": {"q": BOOL_Q},
                "attendu": {"q": False}}

        def rec(label, status, content, final=True):
            return {"label": label, "case_id": "C", "question": "q", "final": final,
                    "http_status": status, "latency_ms": 10.0,
                    "response": {"content": content}}
        records = [rec("LLM-1", 200, '{"reponse": true, "confiance": 0.98}'),
                   rec("LLM-1", 429, None, final=False),
                   rec("LLM-1", 200, '{"reponse": true, "confiance": 0.9}'),
                   rec("LLM-1", 200, 'oui'),
                   rec("LLM-2", 503, None)]
        rows = {r["modele"]: r for r in run_llm.summarize([case], records)}
        self.assertEqual(rows["LLM-1"]["n_appels"], 4)
        self.assertEqual(rows["LLM-1"]["n_parses"], 2)
        self.assertTrue(rows["LLM-1"]["faux_et_sur"])
        self.assertEqual(rows["LLM-1"]["non_parse_raisons"], ["pas du JSON strict"])
        self.assertEqual(rows["LLM-2"]["obtenu"], "NON_PARSE")
        self.assertEqual(rows["LLM-2"]["non_parse_raisons"], ["HTTP 503"])
        md = run_llm.summary_md(list(rows.values()), {
            "run_id": "t", "cases_sha256": "x", "reps": 3, "n_appels": 5,
            "statuts_http": {"200": 3}})
        self.assertIn("| C | q | false | true | 0.94 | 0.90–0.98 | 10.00 | false | true |", md)


class PromptTest(unittest.TestCase):
    def test_prompt_contains_options_and_state(self):
        p = run_llm.build_prompt("ETAT", CHOICE_Q)
        self.assertIn("ETAT", p)
        self.assertIn('- "indetermine" : c', p)
        self.assertIn('{"reponse": <valeur>, "confiance": <nombre entre 0 et 1>}', p)

    def test_pilot_model_same_settings_as_llm2(self):
        m = run_llm.pilot_models("x/y")
        self.assertEqual((m["label"], m["model"]), ("LLM-2", "x/y"))
        self.assertEqual(m["extra"], run_llm.MODELS[1]["extra"])
        items = run_llm.build_items([run_llm.PILOT_CASE], 1, [m])
        self.assertEqual([i["model"]["model"] for i in items], ["x/y"])

    def test_body_limits(self):
        for m in run_llm.MODELS:
            b = run_llm.build_body(m, "s", BOOL_Q)
            self.assertLessEqual(b["max_tokens"], 400)
            self.assertEqual(b["temperature"], 0)
            self.assertNotIn("Authorization", json.dumps(b))


class LeakGuardTest(unittest.TestCase):
    def test_leak_detected_and_neutralized(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "raw.jsonl").write_text('{"x": "abc-SECRET-123"}\n', encoding="utf-8")
            (d / "summary.md").write_text("ok\n", encoding="utf-8")
            self.assertTrue(run_llm.leak_guard(d, "abc-SECRET-123"))
            for p in d.iterdir():
                self.assertEqual(p.read_text(encoding="utf-8"), "FUITE DETECTEE\n")

    def test_no_leak(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "raw.jsonl").write_text('{"x": 1}\n', encoding="utf-8")
            self.assertFalse(run_llm.leak_guard(d, "abc-SECRET-123"))
            self.assertEqual((d / "raw.jsonl").read_text(encoding="utf-8"), '{"x": 1}\n')

    def test_filter_response_drops_everything_else(self):
        body = json.dumps({"id": "gen-1", "model": "m", "provider": "p",
                           "choices": [{"message": {"content": "c", "reasoning": "r"},
                                        "finish_reason": "stop"}],
                           "usage": {"completion_tokens": 3},
                           "providerMetadata": {"gateway": {"generationId": "g"}}})
        self.assertEqual(run_llm.filter_response(200, body),
                         {"model": "m", "content": "c", "finish_reason": "stop",
                          "usage": {"completion_tokens": 3}})
        err = json.dumps({"error": {"message": "m", "type": "t", "param": {"x": 1}}})
        self.assertEqual(run_llm.filter_response(429, err),
                         {"error": {"message": "m", "type": "t"}})

    def test_load_key_quotes_export(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("# c\nOTHER=1\nexport AI_GATEWAY_API_KEY=\"k-1\"\n")
        self.assertEqual(run_llm.load_key(f.name), "k-1")
        Path(f.name).unlink()
        self.assertIsNone(run_llm.load_key("/nonexistent/.env"))


class RunItemsTest(unittest.TestCase):
    """File d'appels : relances 429/503 en fin de file, arret 401/403/404, plafond."""

    case = {"id": "C", "famille": "f", "state": "s", "questions": {"q": BOOL_Q},
            "attendu": {"q": True}}

    def run_with(self, statuses, max_calls=70, reps=1):
        seq = iter(statuses)

        def fake_call(key, body):
            s = next(seq)
            text = '{"choices":[{"message":{"content":"{}"}}]}' if s == 200 else '{"error":{}}'
            return s, 1.0, text, None
        with mock.patch.object(run_llm, "call", fake_call), \
                mock.patch("sys.stdout", io.StringIO()):
            items = run_llm.build_items([self.case], reps)
            return run_llm.run_items("k", items, max_calls, io.StringIO())

    def test_retry_then_give_up(self):
        # 2 modeles x 1 rep ; LLM-1 : 429, 429, 429 (abandon) ; LLM-2 : 200
        recs, arret = self.run_with([429, 200, 429, 429])
        self.assertIsNone(arret)
        l1 = [r for r in recs if r["label"] == "LLM-1"]
        self.assertEqual([r["attempt"] for r in l1], [1, 2, 3])
        self.assertEqual([r["final"] for r in l1], [False, False, True])

    def test_stop_on_403(self):
        recs, arret = self.run_with([403])
        self.assertEqual((len(recs), arret), (1, "stop_http"))

    def test_budget(self):
        recs, arret = self.run_with([200] * 10, max_calls=3, reps=3)
        self.assertEqual((len(recs), arret), (3, "budget"))


if __name__ == "__main__":
    unittest.main()
