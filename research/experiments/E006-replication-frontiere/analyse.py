#!/usr/bin/env python3
"""E006 -- analyse (Python standard) : replication des « faux et sur » d'E005, frontiere
logique (pas, distracteurs), contamination (paires C, E004).

Usage : python3 analyse.py        -> results/analyse.md + results/analyse.json

Lit results/<horodatage>/raw.public.jsonl, HTTP 200 seulement ; parse avec run.extract
d'E001 (importe tel quel). Regles fixees avant tout appel (README, Protocole) :
- conforme : boolean (P >= 0.5) == attendu ; choice == attendu ;
- faux et sur (appel) : non conforme ET (P >= 0.8 si attendu false ; P <= 0.2 si attendu
  true ; P(choix renvoye) >= 0.8 pour un choice) ;
- « replique » (question R) : n >= 5 reponses 200, non conformes >= 80 % des appels, ET la
  mediane de P est du mauvais cote au-dela du seuil (faux et sur a la mediane).
"""
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "E001-jev-sonde"))
import run  # noqa: E402  (extract, num)

# question « faux et sur » d'E005 pour chaque cas R
QUESTION_E005 = {"R-F1-04": "correcte", "R-F1-05": "correcte", "R-F1-08": "correcte",
                 "R-F3-02": "correcte", "R-F4-01": "statut", "R-F4-04": "a_sup_f"}
E005_P = {"R-F1-04": "0.84 / 0.85", "R-F1-05": "0.80", "R-F1-08": "0.86", "R-F3-02": "0.86",
          "R-F4-01": "coherent 0.88 / 0.89", "R-F4-04": "0.15 / 0.19"}


def f2(x):
    return "—" if x is None else "{:.2f}".format(x)


def load(cases):
    by_id = {c["id"]: c for c in cases}
    runs, calls = [], []
    for d in sorted(p for p in (HERE / "results").glob("2026-*") if p.is_dir()):
        recs = [json.loads(l) for l in (d / "raw.public.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        st = {}
        for r in recs:
            st[str(r["http_status"])] = st.get(str(r["http_status"]), 0) + 1
        runs.append({"dossier": d.name, "n": len(recs), "statuts": st,
                     "intervalles": [r["intervalle_s"] for r in recs if r.get("intervalle_s") is not None]})
        for r in recs:
            if r["http_status"] != 200:
                continue
            c = by_id[r["case_id"]]
            if r["request_body"]["state"] != c["state"] or r["request_body"]["questions"] != c["questions"]:
                raise SystemExit("requete differente du cas {} dans {}".format(c["id"], d.name))
            r["_run"] = d.name
            calls.append(r)
    return runs, calls


def evaluate(cases, calls):
    by_id = {c["id"]: c for c in cases}
    ev = []
    for r in calls:
        c = by_id[r["case_id"]]
        for qid, q in c["questions"].items():
            exp = c["attendu"][qid]
            p = run.extract(r["response_body_text"], qid)
            row = {"run": r["_run"], "ts": r["ts"], "case_id": c["id"], "groupe": c["groupe"],
                   "question": qid, "type": q["type"], "attendu": exp}
            if p is None:
                row.update(obtenu="NON_PARSE", p=None, conforme=None, faux_et_sur=None)
            elif q["type"] == "boolean":
                pv = run.num(p.get("probability"))
                got = pv >= 0.5
                row.update(obtenu=got, p=pv, conforme=got == exp,
                           faux_et_sur=(got != exp) and ((exp and pv <= 0.2) or (not exp and pv >= 0.8)))
            else:
                ch, probs = p.get("choice"), p.get("probabilities") or {}
                pc = run.num(probs.get(ch))
                row.update(obtenu=ch, p=pc, p_attendu=run.num(probs.get(exp)),
                           conforme=ch == exp, faux_et_sur=(ch != exp) and pc is not None and pc >= 0.8)
            ev.append(row)
    return ev


def rows_of(ev, cid, qid):
    return [e for e in ev if e["case_id"] == cid and e["question"] == qid and e["obtenu"] != "NON_PARSE"]


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def replique(rs, attendu, typ):
    n = len(rs)
    nc = sum(1 for e in rs if not e["conforme"])
    if typ == "boolean":
        m = med([e["p"] for e in rs])
        extreme = m is not None and ((attendu is True and m <= 0.2) or (attendu is False and m >= 0.8))
    else:
        maj = max({e["obtenu"] for e in rs}, key=lambda v: sum(e["obtenu"] == v for e in rs)) if rs else None
        m = med([e["p"] for e in rs if e["obtenu"] == maj])
        extreme = maj != attendu and m is not None and m >= 0.8
    return n >= 5 and nc >= 0.8 * n and extreme, n, nc, m


def ps(rs, key="p"):
    return " / ".join(f2(e[key]) if e["type"] == "boolean" or key != "p" else "{} {}".format(e["obtenu"], f2(e["p"]))
                      for e in rs)


def main():
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
    by_id = {c["id"]: c for c in cases}
    runs, calls = load(cases)
    ev = evaluate(cases, calls)
    out, js = ["# E006 — analyse (appel par appel, HTTP 200 seulement)", ""], {}

    # --- statuts et rythme
    tot = {}
    for r in runs:
        for k, v in r["statuts"].items():
            tot[k] = tot.get(k, 0) + v
    ints = [i for r in runs for i in r["intervalles"]]
    out += ["## Lancements", "",
            "| dossier | appels | statuts HTTP | intervalle min–max (s) |", "|---|---|---|---|"]
    for r in runs:
        iv = r["intervalles"]
        out.append("| `{}` | {} | {} | {} |".format(
            r["dossier"], r["n"], ", ".join("{}×{}".format(n, s) for s, n in sorted(r["statuts"].items())),
            "{}–{}".format(min(iv), max(iv)) if iv else "— (premier appel)"))
    out += ["", "Total : {} appels ; {} ; intervalles entre départs consécutifs : n = {}, min {} s, max {} s.".format(
        sum(r["n"] for r in runs), ", ".join("{}×{}".format(n, s) for s, n in sorted(tot.items())),
        len(ints), min(ints) if ints else "—", max(ints) if ints else "—"),
        "Évaluations (question × appel 200) : {} ; NON_PARSE : {}.".format(
            len(ev), sum(e["obtenu"] == "NON_PARSE" for e in ev)), ""]
    js["lancements"], js["total_statuts"] = runs, tot

    # --- R
    out += ["## R — réplication des « faux et sûr » d'E005", "",
            "Règle : répliqué si n ≥ 5, non conformes ≥ 80 % et médiane de P du mauvais côté au-delà du seuil (≥ 0.8 si attendu false ; ≤ 0.2 si attendu true ; P(choix) ≥ 0.8 sur un mauvais choix).", "",
            "| cas | question | attendu | E005 | E006 P (par appel) | n | non conformes | faux et sûr (appels) | médiane P | répliqué |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    js["R"] = []
    for cid, qid in QUESTION_E005.items():
        c = by_id[cid]
        rs = rows_of(ev, cid, qid)
        ok, n, nc, m = replique(rs, c["attendu"][qid], c["questions"][qid]["type"])
        fes = sum(1 for e in rs if e["faux_et_sur"])
        out.append("| {} | {} | {} | {} | {} | {} | {}/{} | {} | {} | **{}** |".format(
            cid, qid, json.dumps(c["attendu"][qid]), E005_P[cid], ps(rs), n, nc, n, fes, f2(m),
            "oui" if ok else "non"))
        js["R"].append({"cas": cid, "question": qid, "n": n, "non_conformes": nc, "faux_et_sur": fes,
                        "mediane_p": m, "replique": ok, "p": [e["p"] for e in rs]})
    out += ["", "Autres questions des cas R (non visées par la règle de réplication) :", ""]
    for cid in ("R-F4-01", "R-F4-04"):
        for qid in by_id[cid]["questions"]:
            if qid != QUESTION_E005[cid]:
                rs = rows_of(ev, cid, qid)
                out.append("- {} `{}` (attendu {}) : {} — conformes {}/{}".format(
                    cid, qid, json.dumps(by_id[cid]["attendu"][qid]), ps(rs),
                    sum(e["conforme"] for e in rs), len(rs)))
    out.append("")

    # --- P
    out += ["## P — paires minimales (forme fautive R vs forme correcte P)", "",
            "| paire | P(correcte) forme fautive (R) | médiane | P(correcte) forme correcte (P) | médiane | écart des médianes (correcte − fautive) |",
            "|---|---|---|---|---|---|"]
    js["P"] = []
    for c in [c for c in cases if c["groupe"] == "P"]:
        rf, rc = rows_of(ev, c["paire_de"], "correcte"), rows_of(ev, c["id"], "correcte")
        mf, mc = med([e["p"] for e in rf]), med([e["p"] for e in rc])
        d = None if mf is None or mc is None else mc - mf
        out.append("| {} / {} | {} | {} | {} | {} | {} |".format(
            c["paire_de"], c["id"], ps(rf), f2(mf), ps(rc), f2(mc), "—" if d is None else "{:+.2f}".format(d)))
        js["P"].append({"fautive": c["paire_de"], "correcte": c["id"], "med_fautive": mf, "med_correcte": mc})
    out.append("")

    # --- L pas
    out += ["## L — P(true) en fonction du nombre de pas (chaîne transitive, sans R2)", "",
            "| cas | pas | P(true) par appel | médiane | conformes |", "|---|---|---|---|---|"]
    js["L_pas"] = []
    for c in [c for c in cases if c["famille"] == "L-frontiere-pas"]:
        rs = rows_of(ev, c["id"], "deduction")
        m = med([e["p"] for e in rs])
        out.append("| {} | {} | {} | {} | {}/{} |".format(c["id"], c["pas"], ps(rs), f2(m),
                                                         sum(e["conforme"] for e in rs), len(rs)))
        js["L_pas"].append({"cas": c["id"], "pas": c["pas"], "p": [e["p"] for e in rs], "mediane": m})
    rs = rows_of(ev, "R-F4-04", "a_sup_f")
    out += ["| *R-F4-04 (réf.)* | 4 + incompatible(A, F) + R2 | {} | {} | {}/{} |".format(
        ps(rs), f2(med([e["p"] for e in rs])), sum(e["conforme"] for e in rs), len(rs)), "",
        "L-PAS4 et R-F4-04 ont les mêmes faits dans le même ordre ; seuls `incompatible(A, F)` et la règle 2 diffèrent.", ""]

    # --- L distracteurs
    out += ["## L — statut en fonction du nombre de distracteurs (T1-A, attendu `contradiction`)", "",
            "| cas | distracteurs | choix (P du choix) par appel | P(contradiction) par appel | médiane P(contradiction) | conformes `statut` | P(E > D) médiane |",
            "|---|---|---|---|---|---|---|"]
    js["L_dis"] = []
    serie = [c for c in cases if c["famille"] == "L-frontiere-distracteurs"] + [dict(by_id["R-F4-01"], distracteurs=3)]
    for c in serie:
        rs = rows_of(ev, c["id"], "statut")
        re_ = rows_of(ev, c["id"], "e_sup_d")
        m = med([e["p_attendu"] for e in rs])
        out.append("| {} | {} | {} | {} | {} | {}/{} | {} |".format(
            c["id"], c["distracteurs"], ps(rs), ps(rs, "p_attendu"), f2(m),
            sum(e["conforme"] for e in rs), len(rs), f2(med([e["p"] for e in re_]))))
        js["L_dis"].append({"cas": c["id"], "distracteurs": c["distracteurs"],
                            "p_contradiction": [e["p_attendu"] for e in rs],
                            "choix": [e["obtenu"] for e in rs], "mediane": m})
    out += ["", "Le point à 3 distracteurs est R-F4-01 (état identique à F4-01 d'E005, assertion dans `gen_cases.py`).", ""]

    # --- C
    out += ["## C — contamination (E004) : P(true) avec / sans contradiction indépendante", "",
            "Écart = moyenne P(avec) − moyenne P(sans). Attendu `true` des deux côtés.", "",
            "| paire | P avec (par appel) | moy. avec | P sans (par appel) | moy. sans | écart | conformes avec / sans |",
            "|---|---|---|---|---|---|---|"]
    js["C"], ecarts = [], []
    for pid in sorted({c["paire"] for c in cases if c["groupe"] == "C"}):
        ra, rsn = rows_of(ev, pid + "-avec", "deduction"), rows_of(ev, pid + "-sans", "deduction")
        ma = statistics.mean([e["p"] for e in ra]) if ra else None
        ms = statistics.mean([e["p"] for e in rsn]) if rsn else None
        d = None if ma is None or ms is None else ma - ms
        if d is not None:
            ecarts.append(d)
        out.append("| {} | {} | {} | {} | {} | {} | {}/{} · {}/{} |".format(
            pid, ps(ra), f2(ma), ps(rsn), f2(ms), "—" if d is None else "{:+.3f}".format(d),
            sum(e["conforme"] for e in ra), len(ra), sum(e["conforme"] for e in rsn), len(rsn)))
        js["C"].append({"paire": pid, "p_avec": [e["p"] for e in ra], "p_sans": [e["p"] for e in rsn],
                        "moy_avec": ma, "moy_sans": ms, "ecart": d})
    if ecarts:
        out += ["", "Écart par paire : moyenne {:+.3f}, min {:+.3f}, max {:+.3f} ; signes : {} négatif(s), {} positif(s), {} nul(s).".format(
            statistics.mean(ecarts), min(ecarts), max(ecarts), sum(d < 0 for d in ecarts),
            sum(d > 0 for d in ecarts), sum(d == 0 for d in ecarts))]
        js["C_ecarts"] = ecarts
    out.append("")

    (HERE / "results" / "analyse.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    (HERE / "results" / "analyse.json").write_text(json.dumps(js, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
