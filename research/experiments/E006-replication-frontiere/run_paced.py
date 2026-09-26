#!/usr/bin/env python3
"""E006 -- appels rythmes a Jev (Python standard, zero dependance).

N'implemente PAS l'appel HTTP : run.call, run.load_key, run.leak_guard, run.summarize et
run.summary_md d'E001 sont importes tels quels.

A chaque invocation :
- relit tous les lancements deja faits (results/<horodatage>/raw.jsonl, sinon
  raw.public.jsonl) : reponses 200 par cas, appels consommes (budget), heure du dernier appel ;
- choisit le prochain cas par une regle fixee avant tout appel : groupes dans l'ordre R, C, L,
  P ; dans un groupe, le cas qui a le moins de reponses 200 (egalite : ordre du fichier),
  jusqu'a sa `cible` ;
- attend (time.sleep, interne au script) que --min-interval secondes se soient ecoulees depuis
  le depart de l'appel precedent, y compris celui d'une invocation anterieure ;
- s'arrete a --max-calls appels, au budget total, sur 401/403/404 (code 4), ou apres
  --max-echecs statuts non 200 consecutifs.

Sorties : results/<horodatage>/raw.jsonl (ignore par git), raw.public.jsonl (= raw.jsonl sans
`response_headers`, egalite verifiee), summary.json, summary.md.

Codes : 0 = tous les appels en 200 ; 1 = au moins un statut != 200 ; 2 = cle absente ;
3 = fuite ; 4 = 401/403/404 ; 5 = rien a faire (cibles atteintes ou budget epuise).
"""
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "E001-jev-sonde"))
import run  # noqa: E402  (call, load_key, leak_guard, summarize, summary_md)

ORDRE_GROUPES = "RCLP"
STOP_STATUTS = (401, 403, 404)


def historique(results_dir):
    """Retourne (records de tous les lancements, dans l'ordre des dossiers)."""
    recs = []
    for d in sorted(p for p in Path(results_dir).glob("2026-*") if p.is_dir()):
        for name in ("raw.jsonl", "raw.public.jsonl"):
            f = d / name
            if f.is_file():
                recs += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
                break
    return recs


def prochain_cas(cases, n200):
    """Regle de choix preenregistree. Retourne le cas ou None."""
    for g in ORDRE_GROUPES:
        restants = [c for c in cases if c["groupe"] == g and n200.get(c["id"], 0) < c["cible"]]
        if restants:
            return min(restants, key=lambda c: n200.get(c["id"], 0))  # min stable : ordre du fichier
    return None


def ecrire_public(out_dir):
    """Ecrit raw.public.jsonl (sans response_headers) et verifie l'equivalence ligne a ligne."""
    raw = [json.loads(l) for l in (out_dir / "raw.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    pub = [{k: v for k, v in r.items() if k != "response_headers"} for r in raw]
    (out_dir / "raw.public.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in pub), encoding="utf-8")
    relu = [json.loads(l) for l in (out_dir / "raw.public.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(relu) == len(raw) and all(
        p == {k: v for k, v in r.items() if k != "response_headers"} and "response_headers" not in p
        for p, r in zip(relu, raw)), "raw.public.jsonl non equivalent"
    return len(relu)


def main(argv=None, call=None, now=time.time, sleep=time.sleep, load_key=None):
    call = call or run.call
    load_key = load_key or run.load_key
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--env-file", default="/Users/malik/Documents/EV-LLM/.env")
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--results", default=str(HERE / "results"))
    ap.add_argument("--min-interval", type=float, default=26.0)
    ap.add_argument("--max-calls", type=int, default=8)
    ap.add_argument("--budget", type=int, default=130)
    ap.add_argument("--max-echecs", type=int, default=3)
    args = ap.parse_args(argv)
    if args.min_interval < 26:
        print("--min-interval < 26 s refuse", file=sys.stderr)
        return 2
    if args.max_calls > 8:
        print("--max-calls > 8 refuse", file=sys.stderr)
        return 2

    key = load_key(args.env_file)
    if not key:
        print("{} absente de {}".format(run.KEY_NAME, args.env_file), file=sys.stderr)
        return 2

    cases_bytes = Path(args.cases).read_bytes()
    cases = json.loads(cases_bytes.decode("utf-8"))["cases"]
    by_id = {c["id"]: c for c in cases}
    hist = historique(args.results)
    n200 = {}
    for r in hist:
        if r.get("http_status") == 200:
            n200[r["case_id"]] = n200.get(r["case_id"], 0) + 1
    consommes = len(hist)
    dernier = max((r["t_epoch"] for r in hist if "t_epoch" in r), default=None)

    if consommes >= args.budget or prochain_cas(cases, n200) is None:
        print("rien a faire : {} appels consommes / budget {}".format(consommes, args.budget))
        return 5

    run_id = datetime.fromtimestamp(now()).astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    out_dir = Path(args.results) / run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    records, echecs, code_stop = [], 0, None
    with (out_dir / "raw.jsonl").open("w", encoding="utf-8") as raw:
        while len(records) < args.max_calls and consommes + len(records) < args.budget:
            case = prochain_cas(cases, n200)
            if case is None:
                break
            if dernier is not None:
                attente = args.min_interval - (now() - dernier)
                if attente > 0:
                    sleep(attente)
            t0 = now()
            ecart = None if dernier is None else round(t0 - dernier, 1)
            if ecart is not None and ecart < args.min_interval:
                raise SystemExit("intervalle {} s < {} s : arret".format(ecart, args.min_interval))
            dernier = t0
            body = {"model": run.MODEL, "state": case["state"], "questions": case["questions"]}
            status, lat, headers, text, error = call(key, body)
            rep = n200.get(case["id"], 0) + 1
            rec = {"case_id": case["id"], "rep": rep, "groupe": case["groupe"],
                   "ts": datetime.fromtimestamp(t0).astimezone().isoformat(timespec="seconds"),
                   "t_epoch": t0, "intervalle_s": ecart, "http_status": status,
                   "latency_ms": lat, "request_body": body, "response_headers": headers,
                   "response_body_text": text}
            if error is not None:
                rec["error"] = error
            raw.write(json.dumps(rec, ensure_ascii=False) + "\n")
            raw.flush()
            records.append(rec)
            print("{} {} -> HTTP {} ({} ms, ecart {} s)".format(rec["ts"], case["id"], status, lat, ecart))
            if status == 200:
                n200[case["id"]] = rep
                echecs = 0
            else:
                echecs += 1
            if status in STOP_STATUTS:
                code_stop = 4
                break
            if echecs >= args.max_echecs:
                print("{} echecs consecutifs : fin de l'invocation".format(echecs))
                break

    appeles = [by_id[i] for i in dict.fromkeys(r["case_id"] for r in records)]
    rows = run.summarize(appeles, records)
    meta = {"run_id": run_id, "endpoint": run.ENDPOINT, "model": run.MODEL,
            "reps": "rythme (min {} s), {} appels".format(args.min_interval, len(records)),
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(), "n_appels": len(records),
            "n_http_200": sum(1 for r in records if r["http_status"] == 200),
            "budget_consomme": consommes + len(records), "budget": args.budget}
    (out_dir / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "summary.md").write_text(run.summary_md(rows, meta), encoding="utf-8")
    ecrire_public(out_dir)

    if run.leak_guard(out_dir, key):
        print("FUITE : ne rien committer", file=sys.stderr)
        return 3
    print("resultats : {} ; budget {}/{}".format(out_dir, meta["budget_consomme"], args.budget))
    if code_stop:
        return code_stop
    return 0 if meta["n_http_200"] == meta["n_appels"] else 1


if __name__ == "__main__":
    sys.exit(main())
