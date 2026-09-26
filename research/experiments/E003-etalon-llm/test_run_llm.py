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

    def test_filter_response_drops_everything_else_but_provider(self):
        # Revocation (26/09, Amendement 3, M0019) : ce test figeait l'abandon de "provider" ;
        # le fournisseur reel doit desormais etre journalise. Tout le reste reste abandonne.
        body = json.dumps({"id": "gen-1", "model": "m", "provider": "p",
                           "choices": [{"message": {"content": "c", "reasoning": "r"},
                                        "finish_reason": "stop"}],
                           "usage": {"completion_tokens": 3},
                           "providerMetadata": {"gateway": {"generationId": "g"}}})
        self.assertEqual(run_llm.filter_response(200, body),
                         {"model": "m", "provider": "p", "content": "c", "finish_reason": "stop",
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


class Amendement3Test(unittest.TestCase):
    """Fournisseur impose et journalise, arret net sur 402 (M0019)."""

    case = RunItemsTest.case

    def test_body_only_per_model(self):  # (a)
        expected = {"openai/gpt-4.1-mini": ["openai"], "google/gemini-2.5-flash": ["vertex"]}
        for m in run_llm.with_llm2_max_tokens(run_llm.MODELS, 1200):
            b = run_llm.build_body(m, "s", BOOL_Q)
            self.assertEqual(b.get("providerOptions"),
                             {"gateway": {"only": expected[m["model"]]}})
        self.assertEqual({m["model"] for m in run_llm.MODELS}, set(expected))

    def test_unknown_model_fails_before_call(self):  # (b)
        calls = []
        with mock.patch.object(run_llm, "call", lambda k, b: calls.append(b)), \
                mock.patch("sys.stdout", io.StringIO()):
            items = run_llm.build_items([self.case], 1, [run_llm.pilot_models("x/y")])
            with self.assertRaises(ValueError):
                run_llm.run_items("k", items, 70, io.StringIO())
        self.assertEqual(calls, [])

    def test_unknown_pilot_model_main_exits_7_without_call(self):  # (b), via main
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / ".env"
            env.write_text("AI_GATEWAY_API_KEY=k-test\n", encoding="utf-8")
            argv = ["run_llm.py", "--env-file", str(env), "--pilot", "--pilot-model", "x/y"]
            with mock.patch.object(run_llm, "call", side_effect=AssertionError("appel")) as c, \
                    mock.patch.object(run_llm, "HERE", Path(d)), mock.patch("sys.argv", argv), \
                    mock.patch("sys.stderr", io.StringIO()), \
                    mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(run_llm.main(), 7)
            c.assert_not_called()
            self.assertFalse((Path(d) / "pilot").exists())

    def test_provider_kept_in_public_record(self):  # (c)
        body = json.dumps({"model": "m", "provider": "vertex",
                           "choices": [{"message": {"content": "c"}, "finish_reason": "stop"}]})
        rec = {"label": "LLM-2", "http_status": 200,
               "response": run_llm.filter_response(200, body)}
        with tempfile.TemporaryDirectory() as d:
            run_llm.write_public(d, [rec])
            self.assertEqual(run_llm.load_records([d])[0]["response"].get("provider"), "vertex")
        absent = json.dumps({"choices": [{"message": {"content": "c"}}]})
        self.assertIn("provider", run_llm.filter_response(200, absent))
        self.assertIsNone(run_llm.filter_response(200, absent)["provider"])

    def test_402_stops_without_next_call_exit_6(self):  # (d)
        for prefix in ([402], [429, 402]):  # 402 d'emblee, puis 402 sur une relance
            with self.subTest(prefix=prefix):
                recs, arret = RunItemsTest.run_with(self, prefix + [200] * 10, reps=2)
                self.assertEqual((len(recs), arret), (len(prefix), "quota"))
                self.assertEqual(recs[-1]["http_status"], 402)
                self.assertEqual(run_llm.exit_code(arret, recs), 6)
        self.assertNotIn(402, run_llm.RETRY_STATUSES)

    def test_429_still_retried(self):  # (e)
        recs, arret = RunItemsTest.run_with(self, [429, 200, 200])
        self.assertIsNone(arret)
        l1 = [r for r in recs if r["label"] == "LLM-1"]
        self.assertEqual([(r["http_status"], r["attempt"], r["final"]) for r in l1],
                         [(429, 1, False), (200, 2, True)])
        self.assertEqual(run_llm.exit_code(arret, recs), 0)


class Amendement2Test(unittest.TestCase):
    """Rythmeur (horodatages mockes), selection des manquants, max_tokens de LLM-2."""

    case = {"id": "C", "famille": "f", "state": "s", "questions": {"q": BOOL_Q},
            "attendu": {"q": True}}

    def run_rhythm(self, n, min_interval, last_call=None, call_s=2.0):
        now = [1000.0]
        sleeps = []

        def clock():
            return now[0]

        def sleeper(s):
            sleeps.append(s)
            now[0] += s

        def fake_call(key, body):
            now[0] += call_s  # duree de l'appel
            return 200, call_s * 1000, '{"choices":[{"message":{"content":"{}"}}]}', None
        with mock.patch.object(run_llm, "call", fake_call), \
                mock.patch("sys.stdout", io.StringIO()):
            items = run_llm.build_items([self.case], n, run_llm.MODELS[:1])
            recs, arret = run_llm.run_items("k", items, 70, io.StringIO(), min_interval,
                                            last_call, clock=clock, sleeper=sleeper)
        return recs, sleeps

    def test_rhythm_spaces_call_starts(self):
        recs, sleeps = self.run_rhythm(4, 26.0)
        self.assertEqual(sleeps, [24.0, 24.0, 24.0])
        self.assertEqual([r["interval_s"] for r in recs], [None, 26.0, 26.0, 26.0])

    def test_rhythm_uses_previous_launch(self):
        recs, sleeps = self.run_rhythm(1, 26.0, last_call=990.0)
        self.assertEqual(sleeps, [16.0])
        self.assertEqual(recs[0]["interval_s"], 26.0)
        recs, sleeps = self.run_rhythm(1, 26.0, last_call=900.0)  # deja loin : pas d'attente
        self.assertEqual((sleeps, recs[0]["interval_s"]), ([], 100.0))

    def test_no_rhythm_by_default(self):
        recs, sleeps = self.run_rhythm(3, 0.0)
        self.assertEqual(sleeps, [])

    def test_only_missing_selection(self):
        cases = [self.case]
        m1, m2 = run_llm.MODELS[0]["model"], run_llm.MODELS[1]["model"]

        def rec(model_id, rep, status, content):
            return {"model_id": model_id, "case_id": "C", "question": "q", "rep": rep,
                    "http_status": status, "ts": "2026-09-26T16:00:0{}+02:00".format(rep),
                    "response": {"content": content} if content is not None else None}
        records = [rec(m1, 1, 200, '{"reponse": true, "confiance": 0.9}'),   # repondu
                   rec(m1, 2, 429, None),                                   # manquant
                   rec(m1, 3, 200, '{'),                                    # tronque
                   rec(m2, 1, 200, '{"reponse": false, "confiance": 1}'),   # repondu
                   rec(m2, 2, 200, '{"reponse": true, "confiance": 1}'),    # repondu
                   rec("autre/modele", 3, 200, '{"reponse": true, "confiance": 1}')]
        done = run_llm.answered_keys(cases, records)
        self.assertEqual(done, {(m1, "C", "q", 1), (m2, "C", "q", 1), (m2, "C", "q", 2),
                                ("autre/modele", "C", "q", 3)})
        items = run_llm.build_items(cases, 3, run_llm.MODELS, frozenset(done))
        self.assertEqual([(i["model"]["model"], i["rep"]) for i in items],
                         [(m1, 2), (m1, 3), (m2, 3)])
        self.assertEqual(run_llm.last_call_epoch(records),
                         run_llm.datetime.fromisoformat("2026-09-26T16:00:03+02:00").timestamp())

    def test_load_records_from_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            for i, sub in enumerate(("a", "b")):
                (Path(d) / sub).mkdir()
                (Path(d) / sub / "raw.jsonl").write_text(
                    json.dumps({"i": i}) + "\n\n", encoding="utf-8")
            recs = run_llm.load_records([Path(d) / "a", Path(d) / "b"])
        self.assertEqual(recs, [{"i": 0}, {"i": 1}])

    def test_load_records_prefers_public(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "raw.jsonl").write_text('{"src": "raw"}\n', encoding="utf-8")
            (Path(d) / "raw.public.jsonl").write_text('{"src": "public"}\n', encoding="utf-8")
            self.assertEqual(run_llm.load_records([d]), [{"src": "public"}])
            with self.assertRaises(FileNotFoundError):
                run_llm.load_records([Path(d) / "absent"])

    def test_write_public_whitelist(self):
        rec = {"label": "LLM-1", "http_status": 200, "response": {"content": "c"},
               "response_headers": {"set-cookie": "x"}, "autre": 1}
        with tempfile.TemporaryDirectory() as d:
            run_llm.write_public(d, [rec])
            text = (Path(d) / "raw.public.jsonl").read_text(encoding="utf-8")
            self.assertEqual(run_llm.load_records([d]),
                             [{"label": "LLM-1", "http_status": 200,
                               "response": {"content": "c"}}])
        self.assertNotIn("response_headers", text)
        self.assertNotIn("set-cookie", text)

    def test_max_tokens_llm2_only(self):
        models = run_llm.with_llm2_max_tokens(run_llm.MODELS, 1200)
        b1 = run_llm.build_body(models[0], "s", BOOL_Q)
        b2 = run_llm.build_body(models[1], "s", BOOL_Q)
        self.assertEqual((b1["max_tokens"], b2["max_tokens"]), (400, 1200))
        self.assertEqual(b2["reasoning"], {"effort": "low"})
        self.assertIsNone(run_llm.MODELS[1]["extra"].get("max_tokens"))  # MODELS intact
        self.assertIs(run_llm.with_llm2_max_tokens(run_llm.MODELS, None), run_llm.MODELS)


if __name__ == "__main__":
    unittest.main()
