#!/usr/bin/env python3
"""E005 -- analyse (Python standard) : conformite par famille, liste des « faux et sur »,
calibration grossiere, presence de providerMetadata.typesafe.confidence.

Usage : python3 analyse.py [--cases cases.json] [--out results/analyse.md]

Lit results/<horodatage>/raw.public.jsonl (sinon raw.jsonl), HTTP 200 seulement.
Parse : run.extract d'E001, importe tel quel. Regle de lecture : celle d'E001 (README),
appliquee appel par appel (et non a la mediane, qu'aggregate.py fournit a part) :
- boolean conforme si (P >= 0.5) == attendu ;
- choice conforme si choice == attendu ;
- faux et sur : non conforme ET (P >= 0.8 si attendu false ; P <= 0.2 si attendu true ;
  P(choix renvoye) >= 0.8 pour un choice).
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "E001-jev-sonde"))
import run  # noqa: E402  (extract, num)

BINS = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0000001)]


def bin_label(p):
    for lo, hi in BINS:
        if lo <= p < hi:
            return "{:.1f}–{:.1f}".format(lo, min(hi, 1.0))
    raise ValueError(p)


def load_calls(cases):
    by_id = {c["id"]: c for c in cases}
    calls = []
    for d in sorted((HERE / "results").glob("2026-*")):
        f = d / "raw.public.jsonl"
        if not f.is_file():
            f = d / "raw.jsonl"
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("http_status") != 200:
                continue
            case = by_id[r["case_id"]]
            body = r["request_body"]
            if body["state"] != case["state"] or body["questions"] != case["questions"]:
                raise SystemExit("requete differente du cas {} dans {}".format(case["id"], d.name))
            r["_run"] = d.name
            calls.append(r)
    return calls


def evaluate(cases, calls):
    by_id = {c["id"]: c for c in cases}
    out = []
    for r in calls:
        case = by_id[r["case_id"]]
        body = json.loads(r["response_body_text"])
        tconf = (body.get("providerMetadata") or {}).get("typesafe", {}).get("confidence")
        prov = (body.get("providerMetadata") or {}).get("gateway", {}).get("routing", {}).get("finalProvider")
        for qid, q in case["questions"].items():
            exp = case["attendu"][qid]
            p = run.extract(r["response_body_text"], qid)
            row = {"run": r["_run"], "case_id": case["id"], "famille": case["famille"],
                   "question": qid, "type": q["type"], "attendu": exp, "provider": prov,
                   "typesafe_confidence": tconf.get(qid) if isinstance(tconf, dict) else None}
            if p is None:
                row.update(obtenu="NON_PARSE", p=None, conforme=None, faux_et_sur=None)
            elif q["type"] == "boolean":
                pv = run.num(p.get("probability"))
                got = pv >= 0.5
                conf = got == exp
                row.update(obtenu=got, p=pv, conforme=conf,
                           faux_et_sur=(not conf) and ((exp and pv <= 0.2) or (not exp and pv >= 0.8)),
                           p_reponse=pv if got else 1 - pv)
            else:
                ch = p.get("choice")
                probs = p.get("probabilities") or {}
                pv = run.num(probs.get(ch))
                conf = ch == exp
                row.update(obtenu=ch, p=pv, conforme=conf, probabilities=probs,
                           faux_et_sur=(not conf) and pv is not None and pv >= 0.8,
                           p_reponse=pv)
            out.append(row)
    return out


def pct(k, n):
    return "{}/{} ({:.0f} %)".format(k, n, 100.0 * k / n) if n else "0/0"


def render(cases, rows, statuts):
    L = ["# E005 — analyse (appel par appel, HTTP 200 seulement)", ""]
    L.append("Statuts HTTP par lancement : " + " ; ".join(
        "`{}` {}".format(k, ", ".join("{}×{}".format(n, s) for s, n in sorted(v.items())))
        for k, v in statuts.items()))
    L.append("")
    ok = [r for r in rows if r["conforme"] is not None]
    L += ["Évaluations (question × appel 200) : {} ; NON_PARSE : {}.".format(
        len(ok), sum(1 for r in rows if r["conforme"] is None)), ""]

    L += ["## Conformité par famille", "",
          "| famille | questions | évaluations | conformes | faux et sûr |", "|---|---|---|---|---|"]
    fam = defaultdict(list)
    for r in ok:
        fam[r["famille"]].append(r)
    for f in sorted(fam):
        rs = fam[f]
        nq = len({(r["case_id"], r["question"]) for r in rs})
        L.append("| {} | {} | {} | {} | {} |".format(
            f, nq, len(rs), pct(sum(r["conforme"] for r in rs), len(rs)),
            sum(r["faux_et_sur"] for r in rs)))
    L.append("| **total** | {} | {} | {} | {} |".format(
        len({(r["case_id"], r["question"]) for r in ok}), len(ok),
        pct(sum(r["conforme"] for r in ok), len(ok)), sum(r["faux_et_sur"] for r in ok)))

    L += ["", "## Détail par question", "",
          "| cas | question | attendu | P (par appel) | conformes | faux et sûr |", "|---|---|---|---|---|---|"]
    per_q = defaultdict(list)
    for r in ok:
        per_q[(r["case_id"], r["question"])].append(r)
    for c in cases:
        for qid in c["questions"]:
            rs = per_q.get((c["id"], qid), [])
            ps = " / ".join("—" if r["p"] is None else (
                "{:.2f}".format(r["p"]) if r["type"] == "boolean" else "{} {:.2f}".format(r["obtenu"], r["p"]))
                for r in rs) or "aucune réponse 200"
            L.append("| {} | {} | {} | {} | {} | {} |".format(
                c["id"], qid, json.dumps(c["attendu"][qid]), ps,
                pct(sum(r["conforme"] for r in rs), len(rs)), sum(r["faux_et_sur"] for r in rs)))

    L += ["", "## « Faux et sûr » (le résultat clé)", ""]
    fs = [r for r in ok if r["faux_et_sur"]]
    if not fs:
        L.append("**Aucun** « faux et sûr » sur {} évaluations.".format(len(ok)))
    else:
        L += ["| lancement | cas | question | attendu | obtenu | P |", "|---|---|---|---|---|---|"]
        for r in fs:
            L.append("| {} | {} | {} | {} | {} | {:.2f} |".format(
                r["run"], r["case_id"], r["question"], json.dumps(r["attendu"]),
                json.dumps(r["obtenu"]), r["p"]))
    nc = [r for r in ok if not r["conforme"]]
    L += ["", "Toutes les non-conformités (sûres ou non) : {}.".format(len(nc)), ""]
    for r in nc:
        L.append("- {} {} `{}` : attendu {}, obtenu {}, P = {:.2f}{}".format(
            r["run"], r["case_id"], r["question"], json.dumps(r["attendu"]), json.dumps(r["obtenu"]),
            r["p"], " — **faux et sûr**" if r["faux_et_sur"] else ""))

    L += ["", "## Calibration grossière", "",
          "a) Questions `boolean` : P(true) renvoyée, binnée, contre la part d'attendus `true` et le taux de conformité.", "",
          "| bin P(true) | n | part attendu true | conformes |", "|---|---|---|---|"]
    b = defaultdict(list)
    for r in ok:
        if r["type"] == "boolean":
            b[bin_label(r["p"])].append(r)
    for lo, hi in BINS:
        k = bin_label(lo)
        rs = b.get(k, [])
        L.append("| {} | {} | {} | {} |".format(k, len(rs), pct(sum(r["attendu"] is True for r in rs), len(rs)),
                                                pct(sum(r["conforme"] for r in rs), len(rs))))
    L += ["", "b) Toutes questions : probabilité de la réponse renvoyée (max(P, 1−P) ou P(choix)), binnée, contre le taux de conformité.", "",
          "| bin P(réponse) | n | conformes |", "|---|---|---|"]
    b = defaultdict(list)
    for r in ok:
        if r.get("p_reponse") is not None:
            b[bin_label(r["p_reponse"])].append(r)
    for lo, hi in BINS:
        k = bin_label(lo)
        rs = b.get(k, [])
        L.append("| {} | {} | {} |".format(k, len(rs), pct(sum(r["conforme"] for r in rs), len(rs))))

    L += ["", "## `providerMetadata.typesafe.confidence`", ""]
    ch = [r for r in ok if r["type"] == "choice"]
    L.append("- Questions `choice` : {} évaluations, `confidence` présent sur {}.".format(
        len(ch), sum(r["typesafe_confidence"] is not None for r in ch)))
    for r in ch:
        L.append("  - {} {} : choix {} (P {:.2f}), confidence {}".format(
            r["run"], r["case_id"], r["obtenu"], r["p"], r["typesafe_confidence"]))
    bo = [r for r in ok if r["type"] == "boolean"]
    L.append("- Questions `boolean` : {} évaluations, `confidence` présent sur {}.".format(
        len(bo), sum(r["typesafe_confidence"] is not None for r in bo)))
    prov = defaultdict(int)
    for r in ok:
        prov[r["provider"]] += 1
    L += ["", "Fournisseur final (évaluations) : " + ", ".join("{} ×{}".format(k, v) for k, v in sorted(prov.items(), key=str)), ""]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--out", default=str(HERE / "results" / "analyse.md"))
    a = ap.parse_args()
    cases = json.loads(Path(a.cases).read_text(encoding="utf-8"))["cases"]
    statuts = {}
    for d in sorted((HERE / "results").glob("2026-*")):
        f = d / "raw.public.jsonl"
        if not f.is_file():
            f = d / "raw.jsonl"
        s = defaultdict(int)
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s[str(json.loads(line).get("http_status"))] += 1
        statuts[d.name] = dict(s)
    rows = evaluate(cases, load_calls(cases))
    Path(a.out).write_text(render(cases, rows, statuts), encoding="utf-8")
    (Path(a.out).with_suffix(".json")).write_text(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("analyse :", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
