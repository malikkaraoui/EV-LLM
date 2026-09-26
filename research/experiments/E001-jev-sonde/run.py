#!/usr/bin/env python3
"""E001 -- premiere sonde du modele Jev (TypeSafe AI) via l'AI Gateway Vercel.

Python standard uniquement (>= 3.9), zero dependance.

Securite (depot PUBLIC) :
- la cle AI_GATEWAY_API_KEY est lue en memoire depuis --env-file, jamais affichee,
  jamais ecrite ; l'en-tete Authorization n'est jamais enregistre ;
- apres ecriture, tous les fichiers produits sont relus : si la cle y figure, ils sont
  ecrases par "FUITE DETECTEE" et le script sort en code 3.

Codes de sortie : 0 = tous les appels en HTTP 200 ; 1 = au moins un statut != 200 ;
2 = cle absente ; 3 = fuite detectee.
"""

import argparse
import hashlib
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ENDPOINT = "https://ai-gateway.vercel.sh/v1/evaluate"
MODEL = "typesafe-ai/jev"
KEY_NAME = "AI_GATEWAY_API_KEY"
TIMEOUT_S = 60
HERE = Path(__file__).resolve().parent


def load_key(env_file):
    """Retourne la valeur de AI_GATEWAY_API_KEY, ou None. N'affiche rien du fichier."""
    try:
        lines = Path(env_file).read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name.startswith("export "):
            name = name[len("export "):].strip()
        if name != KEY_NAME:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        return value or None
    return None


def call(key, body):
    """Un POST, sans retry. Retourne (http_status, latency_ms, headers, body_text, error)."""
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "ev-llm-e001-sonde/1.0")
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            raw = resp.read()
            status, headers = resp.status, dict(resp.headers.items())
        error = None
    except urllib.error.HTTPError as e:
        raw = e.read()
        status, headers = e.code, dict(e.headers.items())
        error = None
    except (urllib.error.URLError, OSError) as e:
        # Echec reseau : pas de statut HTTP. Enregistre, jamais relance.
        raw, status, headers = None, None, {}
        error = type(e).__name__ + ": " + str(e)
    latency_ms = round((time.monotonic() - t0) * 1000, 1)
    text = raw.decode("utf-8", errors="replace") if raw is not None else None
    return status, latency_ms, headers, text, error


def extract(body_text, qid):
    """Parse tolerant, forme du guide : answers.<id>.{probability|choice|probabilities|score}.

    Retourne un dict (valeurs trouvees) ou None si la forme differe (NON_PARSE).
    """
    try:
        body = json.loads(body_text)
        ans = body["answers"][qid]
    except (TypeError, ValueError, KeyError):
        return None
    if not isinstance(ans, dict):
        return None
    out = {}
    for k in ("probability", "choice", "probabilities", "score", "confidence"):
        if k in ans:
            out[k] = ans[k]
    if "confidence" not in out:
        try:
            out["confidence"] = body["providerMetadata"]["typesafe"]["confidence"]
        except (TypeError, KeyError):
            pass
    if "probability" not in out and "choice" not in out and "score" not in out:
        return None
    return out


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def summarize(cases, records):
    rows = []
    for case in cases:
        recs = [r for r in records if r["case_id"] == case["id"]]
        lats = [r["latency_ms"] for r in recs if r["http_status"] == 200]
        lat_med = statistics.median(lats) if lats else None
        for qid, q in case["questions"].items():
            expected = case["attendu"].get(qid)
            parsed = [extract(r["response_body_text"], qid) if r["http_status"] == 200 else None
                      for r in recs]
            ok = [p for p in parsed if p is not None]
            row = {"case_id": case["id"], "famille": case["famille"], "question": qid,
                   "type": q["type"], "attendu": expected, "n_appels": len(recs),
                   "n_parses": len(ok), "latence_mediane_ms": lat_med}
            if not ok:
                row.update(obtenu="NON_PARSE", p=None, stabilite=None,
                           conforme=None, faux_et_sur=None)
            elif q["type"] == "boolean":
                ps = [num(p.get("probability")) for p in ok]
                ps = [p for p in ps if p is not None]
                if not ps:
                    row.update(obtenu="NON_PARSE", p=None, stabilite=None,
                               conforme=None, faux_et_sur=None)
                else:
                    med = statistics.median(ps)
                    got = med >= 0.5
                    conforme = got == expected
                    sure_wrong = (not conforme) and ((expected is True and med <= 0.2) or
                                                     (expected is False and med >= 0.8))
                    row.update(obtenu=got, p=med, stabilite=[min(ps), max(ps)],
                               conforme=conforme, faux_et_sur=sure_wrong)
            else:
                # choice (et score) : valeur majoritaire ; P = probabilite du choix renvoye
                # (probabilities[choix]) ou, a defaut, la confiance.
                key = "choice" if q["type"] == "choice" else "score"
                vals = [p.get(key) for p in ok if p.get(key) is not None]
                if not vals:
                    row.update(obtenu="NON_PARSE", p=None, stabilite=None,
                               conforme=None, faux_et_sur=None)
                else:
                    counts = {}
                    for v in vals:
                        counts[json.dumps(v)] = counts.get(json.dumps(v), 0) + 1
                    got = json.loads(max(counts, key=counts.get))
                    ps = []
                    for p in ok:
                        probs = p.get("probabilities")
                        pv = num(probs.get(str(p.get(key)))) if isinstance(probs, dict) else None
                        if pv is None:
                            pv = num(p.get("confidence"))
                        if pv is not None:
                            ps.append(pv)
                    med = statistics.median(ps) if ps else None
                    conforme = got == expected
                    sure_wrong = (not conforme) and med is not None and med >= 0.8
                    row.update(obtenu=got, p=med,
                               stabilite=[min(ps), max(ps)] if ps else None,
                               repartition=counts, conforme=conforme, faux_et_sur=sure_wrong)
            rows.append(row)
    return rows


def fmt(x):
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        return "{:.2f}".format(x)
    return str(x)


def summary_md(rows, meta):
    out = ["# E001 — résumé ({})".format(meta["run_id"]), "",
           "cases.json sha256 : `{}` · répétitions : {} · appels : {} · HTTP 200 : {}".format(
               meta["cases_sha256"], meta["reps"], meta["n_appels"], meta["n_http_200"]), "",
           "| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) "
           "| P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        stab = r["stabilite"]
        stab_s = "—" if not stab else "{}–{}".format(fmt(stab[0]), fmt(stab[1]))
        if r.get("repartition") and len(r["repartition"]) > 1:
            stab_s += " ; choix : " + ", ".join(
                "{}×{}".format(json.loads(k), n) for k, n in r["repartition"].items())
        out.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["case_id"], r["question"], fmt(r["attendu"]), fmt(r["obtenu"]), fmt(r["p"]),
            stab_s, fmt(r["latence_mediane_ms"]), fmt(r["conforme"]), fmt(r["faux_et_sur"])))
    out += ["", "Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente "
            "du guide ; le corps brut est dans raw.jsonl."]
    return "\n".join(out) + "\n"


def leak_guard(out_dir, key):
    """Relit tout ce qui a ete produit ; True si la cle y figure (et neutralise les fichiers)."""
    needle = key.encode("utf-8")
    files = [p for p in out_dir.rglob("*") if p.is_file()]
    leaked = any(needle in p.read_bytes() for p in files)
    if leaked:
        for p in files:
            p.write_text("FUITE DETECTEE\n", encoding="utf-8")
    return leaked


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--env-file", default="/Users/malik/Documents/EV-LLM/.env")
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--reps", type=int, default=3)
    args = ap.parse_args()

    key = load_key(args.env_file)
    if not key:
        print("{} absente de {}".format(KEY_NAME, args.env_file), file=sys.stderr)
        return 2

    cases_bytes = Path(args.cases).read_bytes()
    cases = json.loads(cases_bytes.decode("utf-8"))["cases"]

    run_id = datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    out_dir = HERE / "results" / run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    raw_path = out_dir / "raw.jsonl"

    records = []
    with raw_path.open("w", encoding="utf-8") as raw:
        for case in cases:
            body = {"model": MODEL, "state": case["state"], "questions": case["questions"]}
            for rep in range(1, args.reps + 1):
                ts = datetime.now().astimezone().isoformat(timespec="seconds")
                status, lat, headers, text, error = call(key, body)
                rec = {"case_id": case["id"], "rep": rep, "ts": ts, "http_status": status,
                       "latency_ms": lat, "request_body": body, "response_headers": headers,
                       "response_body_text": text}
                if error is not None:
                    rec["error"] = error
                raw.write(json.dumps(rec, ensure_ascii=False) + "\n")
                raw.flush()
                records.append(rec)
                print("{} rep {} -> HTTP {} ({} ms)".format(case["id"], rep, status, lat))

    rows = summarize(cases, records)
    meta = {"run_id": run_id, "endpoint": ENDPOINT, "model": MODEL, "reps": args.reps,
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
            "n_appels": len(records),
            "n_http_200": sum(1 for r in records if r["http_status"] == 200)}
    (out_dir / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (out_dir / "summary.md").write_text(summary_md(rows, meta), encoding="utf-8")

    if leak_guard(out_dir, key):
        print("FUITE : ne rien committer", file=sys.stderr)
        return 3

    print("resultats : {}".format(out_dir))
    return 0 if meta["n_http_200"] == meta["n_appels"] else 1


if __name__ == "__main__":
    sys.exit(main())
