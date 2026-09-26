#!/usr/bin/env python3
"""E003 -- etalon LLM sur les cas E001, via l'API Chat Completions de l'AI Gateway Vercel.

Python standard uniquement (>= 3.9), zero dependance. Protocole : PROTOCOLE.md.

Securite (depot PUBLIC) :
- la cle AI_GATEWAY_API_KEY est lue en memoire depuis --env-file, jamais affichee,
  jamais ecrite ; aucun en-tete (requete ou reponse) n'est enregistre ;
- de la reponse, seuls model, choices[0].message.content, finish_reason et usage sont gardes ;
- apres ecriture, tous les fichiers produits sont relus : si la cle y figure, ils sont
  ecrases par "FUITE DETECTEE" et le script sort en code 3.

Amendement 2 (M0010) : --min-interval (rythmeur interne, limite fournisseur de 5 req/min),
--only-missing (ne rejoue que les elements sans reponse 200 parsable dans des dossiers donnes),
--max-tokens-llm2 (max_tokens de LLM-2 seul), --summarize-dirs (resume consolide, zero appel).

Codes de sortie : 0 = tous les elements en HTTP 200 ; 1 = au moins un element sans 200 ;
2 = cle absente ; 3 = fuite detectee ; 4 = arret sur 401/403/404 ; 5 = plafond d'appels atteint.
"""

import argparse
import hashlib
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import deque
from datetime import datetime
from pathlib import Path

ENDPOINT = "https://ai-gateway.vercel.sh/v1/chat/completions"
KEY_NAME = "AI_GATEWAY_API_KEY"
TIMEOUT_S = 60
MAX_TOKENS = 400
MAX_RETRIES = 2
RETRY_STATUSES = (429, 503)
STOP_STATUSES = (401, 403, 404)
HERE = Path(__file__).resolve().parent

MODELS = [
    {"label": "LLM-1", "model": "openai/gpt-4.1-mini", "extra": {}},
    # Amendement 1 (26/09, PROTOCOLE.md) : google/gemini-3.8-flash refuse en 403 (free tier).
    {"label": "LLM-2", "model": "google/gemini-2.5-flash",
     "extra": {"reasoning": {"effort": "low"}}},
]

PILOT_CASE = {
    "id": "PILOTE", "famille": "pilote-hors-evaluation",
    "state": "Faits : tout carré est un rectangle. X est un carré.",
    "questions": {"x_rectangle": {"type": "boolean",
                                  "instructions": "Peut-on déduire que X est un rectangle ?"}},
    "attendu": {"x_rectangle": True},
}

PROMPT = (
    "Tu réponds à une question de raisonnement. Réponds UNIQUEMENT par un objet JSON strict, "
    "sans aucun texte autour et sans bloc de code, de la forme :\n"
    "{{\"reponse\": <valeur>, \"confiance\": <nombre entre 0 et 1>}}\n\n"
    "Énoncé :\n{state}\n\n"
    "Question :\n{instructions}\n\n"
    "{bloc_options}\n"
    "\"confiance\" est ta probabilité (entre 0 et 1) que ta réponse soit correcte."
)


def pilot_models(model_id):
    """Candidat LLM-2 pour un pilote (Amendement 1) : memes reglages que LLM-2."""
    return {"label": "LLM-2", "model": model_id, "extra": dict(MODELS[1]["extra"])}


def with_llm2_max_tokens(models, max_tokens):
    """Amendement 2 : max_tokens propre a LLM-2 (None = inchange). Les autres modeles intacts."""
    if max_tokens is None:
        return models
    out = []
    for m in models:
        if m["label"] == "LLM-2":
            m = dict(m, extra=dict(m["extra"], max_tokens=max_tokens))
        out.append(m)
    return out


def load_records(dirs):
    """Enregistrements raw.jsonl des dossiers donnes (ordre des dossiers, puis des lignes)."""
    records = []
    for d in dirs:
        with (Path(d) / "raw.jsonl").open(encoding="utf-8") as f:
            records += [json.loads(line) for line in f if line.strip()]
    return records


def answered_keys(cases, records):
    """(model_id, cas, question, repetition) ayant deja une reponse HTTP 200 parsable."""
    questions = {(c["id"], qid): q for c in cases for qid, q in c["questions"].items()}
    done = set()
    for r in records:
        q = questions.get((r.get("case_id"), r.get("question")))
        if q is None or r.get("http_status") != 200 or not r.get("response"):
            continue
        if parse_answer(r["response"].get("content"), q)[2] is None:
            done.add((r["model_id"], r["case_id"], r["question"], r["rep"]))
    return done


def last_call_epoch(records):
    """Horodatage (epoch s) du dernier appel journalise, ou None."""
    stamps = [datetime.fromisoformat(r["ts"]).timestamp() for r in records if r.get("ts")]
    return max(stamps) if stamps else None


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


def build_prompt(state, question):
    if question["type"] == "choice":
        lines = ["\"reponse\" doit être exactement une de ces chaînes :"]
        lines += ["- \"{}\" : {}".format(k, v) for k, v in question["criteria"].items()]
        bloc = "\n".join(lines) + "\n"
    else:
        bloc = "\"reponse\" doit être le booléen JSON true ou false.\n"
    return PROMPT.format(state=state, instructions=question["instructions"], bloc_options=bloc)


def build_body(model_cfg, state, question):
    body = {"model": model_cfg["model"],
            "messages": [{"role": "user", "content": build_prompt(state, question)}],
            "temperature": 0, "max_tokens": MAX_TOKENS,
            "response_format": {"type": "json_object"}}
    body.update(model_cfg["extra"])
    return body


def call(key, body):
    """Un POST. Retourne (http_status, latency_ms, body_text, error). Aucun en-tete garde."""
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "ev-llm-e003-etalon/1.0")
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            raw, status, error = resp.read(), resp.status, None
    except urllib.error.HTTPError as e:
        raw, status, error = e.read(), e.code, None
    except (urllib.error.URLError, OSError) as e:
        raw, status, error = None, None, type(e).__name__ + ": " + str(e)
    latency_ms = round((time.monotonic() - t0) * 1000, 1)
    text = raw.decode("utf-8", errors="replace") if raw is not None else None
    return status, latency_ms, text, error


def filter_response(status, text):
    """Garde model / content / finish_reason / usage (200) ou le seul objet error (sinon)."""
    try:
        body = json.loads(text)
    except (TypeError, ValueError):
        return {"non_json": (text or "")[:500]}
    if not isinstance(body, dict):
        return {"non_json": str(body)[:500]}
    if status == 200:
        choice = (body.get("choices") or [{}])[0] or {}
        msg = choice.get("message") or {}
        return {"model": body.get("model"), "content": msg.get("content"),
                "finish_reason": choice.get("finish_reason"), "usage": body.get("usage")}
    err = body.get("error")
    if isinstance(err, dict):
        return {"error": {k: err.get(k) for k in ("message", "type", "code") if k in err}}
    return {"error": str(err)[:500]}


def parse_answer(content, question):
    """Parse strict. Retourne (reponse, confiance, None) ou (None, None, raison)."""
    if not isinstance(content, str):
        return None, None, "contenu absent"
    try:
        obj = json.loads(content.strip())
    except ValueError:
        return None, None, "pas du JSON strict"
    if not isinstance(obj, dict) or set(obj) != {"reponse", "confiance"}:
        return None, None, "cles differentes de {reponse, confiance}"
    rep, conf = obj["reponse"], obj["confiance"]
    if isinstance(conf, bool) or not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
        return None, None, "confiance hors [0,1] ou non numerique"
    if question["type"] == "boolean":
        if not isinstance(rep, bool):
            return None, None, "reponse non booleenne"
    elif not isinstance(rep, str) or rep not in question["criteria"]:
        return None, None, "reponse hors options"
    return rep, float(conf), None


def aggregate(expected, parsed):
    """parsed = liste de (reponse, confiance) des repetitions parsees. Regle de PROTOCOLE.md."""
    if not parsed:
        return {"obtenu": "NON_PARSE", "p": None, "stabilite": None, "repartition": None,
                "conforme": None, "faux_et_sur": None, "n_faux_et_sur_reps": 0}
    counts = {}
    for rep, _ in parsed:
        counts[json.dumps(rep)] = counts.get(json.dumps(rep), 0) + 1
    top = max(counts.values())
    leaders = [k for k, n in counts.items() if n == top]
    confs = [c for _, c in parsed]
    n_fs = sum(1 for rep, c in parsed if rep != expected and c >= 0.8)
    base = {"stabilite": [min(confs), max(confs)], "repartition": counts,
            "n_faux_et_sur_reps": n_fs}
    if len(leaders) > 1:
        base.update(obtenu="INSTABLE", p=None, conforme=False, faux_et_sur=False)
        return base
    got = json.loads(leaders[0])
    p = round(statistics.median([c for rep, c in parsed if rep == got]), 6)  # 0.7999.. -> 0.8
    conforme = got == expected
    base.update(obtenu=got, p=p, conforme=conforme, faux_et_sur=(not conforme) and p >= 0.8)
    return base


def summarize(cases, records, models=MODELS):
    rows = []
    for m in models:
        for case in cases:
            for qid, q in case["questions"].items():
                recs = [r for r in records if r["label"] == m["label"]
                        and r["case_id"] == case["id"] and r["question"] == qid]
                finals = [r for r in recs if r.get("final")]
                parsed, reasons = [], []
                for r in finals:
                    if r["http_status"] != 200:
                        reasons.append("HTTP {}".format(r["http_status"]))
                        continue
                    rep, conf, why = parse_answer(r["response"].get("content"), q)
                    if why:
                        reasons.append(why)
                    else:
                        parsed.append((rep, conf))
                lats = [r["latency_ms"] for r in finals if r["http_status"] == 200]
                row = {"modele": m["label"], "model_id": m["model"], "case_id": case["id"],
                       "famille": case["famille"], "question": qid, "type": q["type"],
                       "attendu": case["attendu"].get(qid), "n_appels": len(recs),
                       "n_parses": len(parsed), "non_parse_raisons": reasons,
                       "latence_mediane_ms": statistics.median(lats) if lats else None}
                row.update(aggregate(case["attendu"].get(qid), parsed))
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


def summary_md(rows, meta, models=MODELS):
    out = ["# E003 — résumé ({})".format(meta["run_id"]), "",
           "cases.json sha256 : `{}` · répétitions : {} · appels : {} · statuts : {}".format(
               meta["cases_sha256"], meta["reps"], meta["n_appels"],
               json.dumps(meta["statuts_http"])), ""]
    for m in models:
        out += ["## {} — `{}`".format(m["label"], m["model"]), "",
                "| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) "
                "| P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme "
                "| faux et sûr |",
                "|---|---|---|---|---|---|---|---|---|"]
        for r in (r for r in rows if r["modele"] == m["label"]):
            stab = r["stabilite"]
            stab_s = "—" if not stab else "{}–{}".format(fmt(stab[0]), fmt(stab[1]))
            if r.get("repartition") and len(r["repartition"]) > 1:
                stab_s += " ; choix : " + ", ".join(
                    "{}×{}".format(json.loads(k), n) for k, n in r["repartition"].items())
            out.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                r["case_id"], r["question"], fmt(r["attendu"]), fmt(r["obtenu"]), fmt(r["p"]),
                stab_s, fmt(r["latence_mediane_ms"]), fmt(r["conforme"]),
                fmt(r["faux_et_sur"])))
        out.append("")
    out += ["Règle de lecture : PROTOCOLE.md. « P ou confiance » = confiance **verbalisée** "
            "(médiane sur les répétitions majoritaires). `NON_PARSE` : raisons dans summary.json."]
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


def build_items(cases, reps, models=MODELS, skip=frozenset()):
    """File des elements ; skip = cles (model_id, cas, question, rep) deja repondues."""
    return deque({"model": m, "case": c, "qid": qid, "rep": rep, "attempt": 0}
                 for m in models for c in cases for qid in c["questions"]
                 for rep in range(1, reps + 1)
                 if (m["model"], c["id"], qid, rep) not in skip)


def run_items(key, items, max_calls, raw, min_interval=0.0, last_call=None,
              clock=time.time, sleeper=time.sleep):
    """Execute la file. Retourne (records, arret) ; arret in (None, 'stop_http', 'budget').

    min_interval (Amendement 2) : ecart minimal en secondes entre les debuts de deux appels,
    y compris avec last_call (epoch du dernier appel d'un lancement precedent). 0 = pas d'attente.
    """
    records, n_calls = [], 0
    while items:
        if n_calls >= max_calls:
            return records, "budget"
        it = items.popleft()
        q = it["case"]["questions"][it["qid"]]
        body = build_body(it["model"], it["case"]["state"], q)
        if min_interval > 0 and last_call is not None:
            wait = min_interval - (clock() - last_call)
            if wait > 0:
                sleeper(wait)
        start = clock()
        interval = None if last_call is None else round(start - last_call, 1)
        last_call = start
        ts = datetime.now().astimezone().isoformat(timespec="seconds")
        status, lat, text, error = call(key, body)
        n_calls += 1
        it["attempt"] += 1
        retry = status in RETRY_STATUSES and it["attempt"] <= MAX_RETRIES
        rec = {"label": it["model"]["label"], "model_id": it["model"]["model"],
               "case_id": it["case"]["id"], "question": it["qid"], "rep": it["rep"],
               "attempt": it["attempt"], "final": not retry, "ts": ts, "http_status": status,
               "latency_ms": lat, "interval_s": interval, "request_body": body,
               "response": filter_response(status, text) if text is not None else None}
        if error is not None:
            rec["error"] = error
        raw.write(json.dumps(rec, ensure_ascii=False) + "\n")
        raw.flush()
        records.append(rec)
        print("{} {} {} rep {} essai {} -> HTTP {} ({} ms)".format(
            rec["label"], rec["case_id"], rec["question"], rec["rep"], rec["attempt"],
            status, lat))
        if status in STOP_STATUSES:
            return records, "stop_http"
        if retry:
            items.append(it)  # relance espacee par le reste de la file, jamais par une attente
    return records, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--env-file", default="/Users/malik/Documents/EV-LLM/.env")
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--max-calls", type=int, default=65)
    ap.add_argument("--pilot", action="store_true", help="un appel par modele, hors cases.json")
    ap.add_argument("--pilot-model", default=None,
                    help="avec --pilot : un seul appel, LLM-2 remplace par ce modele (Amendement 1)")
    ap.add_argument("--min-interval", type=float, default=0.0,
                    help="secondes minimales entre deux appels (Amendement 2 ; 0 = aucune attente)")
    ap.add_argument("--only-missing", nargs="+", default=None, metavar="DOSSIER",
                    help="ne rejoue que les elements sans reponse 200 parsable dans ces dossiers")
    ap.add_argument("--max-tokens-llm2", type=int, default=None,
                    help="max_tokens de LLM-2 seul (Amendement 2 ; defaut : {})".format(MAX_TOKENS))
    ap.add_argument("--summarize-dirs", nargs="+", default=None, metavar="DOSSIER",
                    help="aucun appel : resume consolide des raw.jsonl de ces dossiers")
    args = ap.parse_args()

    if args.summarize_dirs:
        return summarize_dirs(args)

    key = load_key(args.env_file)
    if not key:
        print("{} absente de {}".format(KEY_NAME, args.env_file), file=sys.stderr)
        return 2

    models = MODELS
    if args.pilot_model:
        if not args.pilot:
            print("--pilot-model exige --pilot", file=sys.stderr)
            return 2
        models = [pilot_models(args.pilot_model)]
    models = with_llm2_max_tokens(models, args.max_tokens_llm2)
    cases_bytes = Path(args.cases).read_bytes()
    if args.pilot:
        cases, reps, sub = [PILOT_CASE], 1, "pilot"
    else:
        cases, reps, sub = json.loads(cases_bytes.decode("utf-8"))["cases"], args.reps, "results"

    skip, last_call = frozenset(), None
    if args.only_missing:
        previous = load_records(args.only_missing)
        skip, last_call = frozenset(answered_keys(cases, previous)), last_call_epoch(previous)
    items = build_items(cases, reps, models, skip)
    n_items = len(items)
    print("elements a jouer : {} (deja repondus : {})".format(n_items, len(skip)))

    run_id = datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    out_dir = HERE / sub / run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    with (out_dir / "raw.jsonl").open("w", encoding="utf-8") as raw:
        records, arret = run_items(key, items, args.max_calls, raw,
                                   args.min_interval, last_call)

    statuts = {}
    for r in records:
        statuts[str(r["http_status"])] = statuts.get(str(r["http_status"]), 0) + 1
    rows = summarize(cases, records, models)
    meta = {"run_id": run_id, "endpoint": ENDPOINT, "reps": reps, "pilot": args.pilot,
            "models": models, "max_tokens": MAX_TOKENS, "max_calls": args.max_calls,
            "min_interval_s": args.min_interval, "only_missing": args.only_missing,
            "n_elements_a_jouer": n_items, "n_deja_repondus": len(skip),
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
            "n_appels": len(records), "statuts_http": statuts, "arret": arret}
    (out_dir / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (out_dir / "summary.md").write_text(summary_md(rows, meta, models), encoding="utf-8")

    if leak_guard(out_dir, key):
        print("FUITE : ne rien committer", file=sys.stderr)
        return 3

    print("resultats : {} · appels : {} · statuts : {} · arret : {}".format(
        out_dir, len(records), statuts, arret))
    if arret == "stop_http":
        return 4
    if arret == "budget":
        return 5
    finals = [r for r in records if r["final"]]
    return 0 if all(r["http_status"] == 200 for r in finals) else 1


def summarize_dirs(args):
    """Resume consolide (zero appel) : toutes les reponses finales des dossiers donnes.

    Seuls les modeles d'evaluation (MODELS) sont gardes ; le max_tokens reellement envoye
    reste lisible dans chaque request_body. Ecrit results/consolide/summary.{json,md}.
    """
    cases_bytes = Path(args.cases).read_bytes()
    cases = json.loads(cases_bytes.decode("utf-8"))["cases"]
    records = load_records(args.summarize_dirs)
    ids = {m["model"] for m in MODELS}
    records = [r for r in records if r["model_id"] in ids]
    statuts = {}
    for r in records:
        statuts[str(r["http_status"])] = statuts.get(str(r["http_status"]), 0) + 1
    rows = summarize(cases, records)
    meta = {"run_id": "consolide", "dossiers": args.summarize_dirs, "reps": args.reps,
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
            "n_appels": len(records), "statuts_http": statuts}
    out = HERE / "results" / "consolide"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (out / "summary.md").write_text(summary_md(rows, meta), encoding="utf-8")
    print("resume consolide : {} · appels : {} · statuts : {}".format(out, len(records), statuts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
