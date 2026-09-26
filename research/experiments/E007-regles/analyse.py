#!/usr/bin/env python3
"""E007 -- analyse (Python standard) : ablation de regles (A), distracteurs isoles (B), regle
d'accord ecrite (C), controles (D).

Usage : python3 analyse.py        -> results/analyse.md + results/analyse.json

Lit results/<horodatage>/raw.public.jsonl (HTTP 200 seulement ; requete verifiee egale au cas),
parse avec run.extract d'E001 (importe tel quel). Reference « sans regle » pour C : les
raw.public.jsonl d'E006 (cas R-F1-0x et P-F1-0x), lus sans modification.
Regles de lecture fixees avant tout appel (README, « Regles de lecture ») :
- mesure = mediane par cas de P(true) (booleen) ou P(contradiction) (question `statut`) ;
- « change » : |delta| >= 0.30 ; « ne change pas » : |delta| < 0.15 ; sinon « ambigu » ;
- A : lit la regle si (ii), (iii), (iv) changent dans le sens attendu (baisse) et (v) ne change
  pas ; ne la lit pas si aucune de (ii)/(iii)/(iv) ne change ; sinon partiellement ;
- B : distracteur « tue » la contradiction si mediane P(contradiction) < 0.5 ;
- C : corrige sur une paire si, avec regle, P(correcte) >= 0.5 pour la forme correcte ET < 0.5
  pour la forme fautive.
"""
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
E006 = HERE.parent / "E006-replication-frontiere"
sys.path.insert(0, str(HERE.parent / "E001-jev-sonde"))
import run  # noqa: E402  (extract, num)

CHANGE, STABLE = 0.30, 0.15


def f2(x):
    return "—" if x is None else "{:.2f}".format(x)


def fd(x):
    return "—" if x is None else "{:+.2f}".format(x)


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def load(exp_dir, cases, strict=True):
    """Retourne (lancements, evaluations). Une evaluation = un couple (appel 200, question)."""
    by_id = {c["id"]: c for c in cases}
    runs, ev = [], []
    for d in sorted(p for p in (exp_dir / "results").glob("2026-*") if p.is_dir()):
        if not (d / "raw.public.jsonl").is_file():
            raise SystemExit("{} : raw.public.jsonl absent (lancement en cours ?)".format(d.name))
        recs = [json.loads(l) for l in (d / "raw.public.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        st = {}
        for r in recs:
            st[str(r["http_status"])] = st.get(str(r["http_status"]), 0) + 1
        runs.append({"dossier": d.name, "n": len(recs), "statuts": st,
                     "intervalles": [r["intervalle_s"] for r in recs if r.get("intervalle_s") is not None],
                     "ts": [r["ts"] for r in recs]})
        for r in recs:
            if r["http_status"] != 200 or r["case_id"] not in by_id:
                continue
            c = by_id[r["case_id"]]
            if strict and (r["request_body"]["state"] != c["state"] or r["request_body"]["questions"] != c["questions"]):
                raise SystemExit("requete differente du cas {} dans {}".format(c["id"], d.name))
            for qid, q in c["questions"].items():
                p = run.extract(r["response_body_text"], qid)
                e = {"run": d.name, "ts": r["ts"], "case_id": c["id"], "question": qid, "type": q["type"],
                     "attendu": c["attendu"][qid]}
                if p is None:
                    e.update(obtenu="NON_PARSE", p=None, conforme=None)
                elif q["type"] == "boolean":
                    pv = run.num(p.get("probability"))
                    e.update(obtenu=pv >= 0.5, p=pv, conforme=(pv >= 0.5) == c["attendu"][qid])
                else:
                    probs = p.get("probabilities") or {}
                    e.update(obtenu=p.get("choice"), p=run.num(probs.get("contradiction")),
                             p_choix=run.num(probs.get(p.get("choice"))),
                             conforme=p.get("choice") == c["attendu"][qid])
                ev.append(e)
    return runs, ev


def sel(ev, cid, qid):
    return [e for e in ev if e["case_id"] == cid and e["question"] == qid and e["obtenu"] != "NON_PARSE"]


def ps(rs):
    return " / ".join(f2(e["p"]) for e in rs) or "—"


def choix(rs):
    return " / ".join("{} {}".format(e["obtenu"], f2(e["p_choix"])) for e in rs) or "—"


def qualif(delta):
    if delta is None:
        return "—"
    a = abs(delta)
    return "change" if a >= CHANGE else ("ne change pas" if a < STABLE else "ambigu")


def main():
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
    by_id = {c["id"]: c for c in cases}
    runs, ev = load(HERE, cases)
    e6_cases = json.loads((E006 / "cases.json").read_text(encoding="utf-8"))["cases"]
    _, ev6 = load(E006, e6_cases)
    out, js = ["# E007 — analyse (appel par appel, HTTP 200 seulement)", ""], {}

    # --- lancements
    tot, ints = {}, []
    out += ["## Lancements", "", "| dossier | appels | statuts HTTP | intervalle min–max (s) |", "|---|---|---|---|"]
    for r in runs:
        for k, v in r["statuts"].items():
            tot[k] = tot.get(k, 0) + v
        ints += r["intervalles"]
        iv = r["intervalles"]
        out.append("| `{}` | {} | {} | {} |".format(
            r["dossier"], r["n"], ", ".join("{}×{}".format(v, k) for k, v in sorted(r["statuts"].items())),
            "{:.1f}–{:.1f}".format(min(iv), max(iv)) if iv else "—"))
    n_app = sum(r["n"] for r in runs)
    premier = min((t for r in runs for t in r["ts"]), default=None)
    out += ["", "Total : {} appels ; {} ; intervalles entre départs consécutifs : n = {}, min {} s, max {} s ; premier appel {}.".format(
        n_app, ", ".join("{}×{}".format(v, k) for k, v in sorted(tot.items())), len(ints),
        min(ints) if ints else "—", max(ints) if ints else "—", premier),
        "Évaluations (question × appel 200) : {} ; NON_PARSE : {}.".format(
            len(ev), sum(1 for e in ev if e["obtenu"] == "NON_PARSE")), ""]
    js["lancements"] = {"n_appels": n_app, "statuts": tot, "intervalle_min": min(ints) if ints else None,
                        "intervalle_max": max(ints) if ints else None, "premier_appel": premier}

    # --- D
    out += ["## D — contrôles", "", "| cas | question | attendu | P par appel | médiane | conformes |", "|---|---|---|---|---|---|"]
    js["D"] = {}
    for c in [c for c in cases if c["groupe"] == "D"]:
        for qid in c["questions"]:
            rs = sel(ev, c["id"], qid)
            m = med([e["p"] for e in rs])
            nc = sum(e["conforme"] for e in rs)
            out.append("| {} | {} | {} | {} | {} | {}/{} |".format(c["id"], qid, json.dumps(c["attendu"][qid]), ps(rs), f2(m), nc, len(rs)))
            js["D"][c["id"]] = {"mediane": m, "conformes": nc, "n": len(rs)}

    # --- C
    out += ["", "## C — règle d'accord écrite dans l'état", "",
            "Mesure : P(correcte). « sans règle » = E006 (forme fautive : R-F1-0x, 5 appels ; forme correcte : P-F1-0x, 3 appels) et rappel C0 d'E007 (forme correcte, 2 appels, même état qu'E006).", "",
            "| paire | forme | attendu | sans règle E006 (par appel) | méd. | rappel C0 (par appel) | méd. | avec règle (par appel) | méd. | Δ (avec − sans E006) | conformes avec règle |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    js["C"] = {}
    for src in ("F1-04", "F1-05", "F1-08"):
        js["C"][src] = {}
        for forme in ("fautive", "correcte"):
            c = by_id["C-{}-{}".format(src, forme)]
            rs = sel(ev, c["id"], "correcte")
            r6 = sel(ev6, c["sans_regle_e006"], "correcte")
            r0 = sel(ev, "C0-{}-correcte".format(src), "correcte") if forme == "correcte" else []
            m, m6, m0 = med([e["p"] for e in rs]), med([e["p"] for e in r6]), med([e["p"] for e in r0])
            d = None if m is None or m6 is None else m - m6
            nc = sum(e["conforme"] for e in rs)
            out.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}/{} |".format(
                src, forme, json.dumps(c["attendu"]["correcte"]), ps(r6), f2(m6), ps(r0) if r0 else "—",
                f2(m0), ps(rs), f2(m), fd(d), nc, len(rs)))
            js["C"][src][forme] = {"avec": m, "sans_e006": m6, "rappel_c0": m0, "delta": d, "conformes": nc, "n": len(rs)}
        f, co = js["C"][src]["fautive"]["avec"], js["C"][src]["correcte"]["avec"]
        js["C"][src]["corrige"] = f is not None and co is not None and co >= 0.5 and f < 0.5
        js["C"][src]["ordre_avec"] = None if f is None or co is None else co - f
    out += ["", "| paire | P(correcte) avec règle : correcte − fautive | sans règle (E006) : correcte − fautive | corrige son jugement (règle) |", "|---|---|---|---|"]
    for src, v in js["C"].items():
        s6 = None if v["correcte"]["sans_e006"] is None else v["correcte"]["sans_e006"] - v["fautive"]["sans_e006"]
        out.append("| {} | {} | {} | **{}** |".format(src, fd(v["ordre_avec"]), fd(s6), "oui" if v["corrige"] else "non"))

    # --- A
    out += ["", "## A — ablation de règle", "",
            "Mesure : médiane de P(contradiction) pour A1 `statut`, de P(true) pour A1 `e_sup_d` et A2 `deduction`. Δ = variante − (i). « change » |Δ| ≥ 0.30, « ne change pas » |Δ| < 0.15.", ""]
    js["A"] = {}
    for base, qid, desc in (("A1", "statut", "T1-A, R2 manipulée — P(contradiction)"),
                            ("A1", "e_sup_d", "T1-A, R2 manipulée — P(E > D) (attendu true partout)"),
                            ("A2", "deduction", "chaîne A > B > C > D, R1 manipulée — P(A > D)")):
        out += ["### {} — {}".format(base, desc), "",
                "| variante | attendu | {}P par appel | médiane | Δ vs (i) | lecture | conformes |".format("choix (P du choix) | " if qid == "statut" else ""),
                "|---|---|{}---|---|---|---|---|".format("---|" if qid == "statut" else "")]
        ref = med([e["p"] for e in sel(ev, base + "-i", qid)])
        js["A"]["{}-{}".format(base, qid)] = {}
        for suf in ("i", "ii", "iii", "iv", "v"):
            cid = "{}-{}".format(base, suf)
            rs = sel(ev, cid, qid)
            m = med([e["p"] for e in rs])
            d = None if suf == "i" or m is None or ref is None else m - ref
            nc = sum(e["conforme"] for e in rs)
            out.append("| {} ({}) | {} | {}{} | {} | {} | {} | {}/{} |".format(
                suf, by_id[cid]["justification"].split(" : ")[1].split(".")[0] if base == "A1" else by_id[cid]["justification"].split("R1 : ")[1].split(".")[0],
                json.dumps(by_id[cid]["attendu"][qid]), choix(rs) + " | " if qid == "statut" else "", ps(rs), f2(m),
                fd(d), "référence" if suf == "i" else qualif(d), nc, len(rs)))
            js["A"]["{}-{}".format(base, qid)][suf] = {"mediane": m, "delta": d, "conformes": nc, "n": len(rs)}
        out.append("")
    for key in ("A1-statut", "A2-deduction"):
        v = js["A"][key]
        baisse = {s: v[s]["delta"] is not None and v[s]["delta"] <= -CHANGE for s in ("ii", "iii", "iv")}
        stable = {s: v[s]["delta"] is not None and abs(v[s]["delta"]) < STABLE for s in ("ii", "iii", "iv")}
        v_ok = v["v"]["delta"] is not None and abs(v["v"]["delta"]) < STABLE
        if any(v[s]["delta"] is None for s in ("ii", "iii", "iv", "v")):
            verdict = "donnees insuffisantes"
        elif all(baisse.values()) and v_ok:
            verdict = "lit la règle"
        elif all(stable.values()):
            verdict = "ne lit pas la règle"
        else:
            verdict = "partiellement"
        v["verdict"] = verdict
        v["detail"] = {"baisse_ii_iii_iv": baisse, "v_ne_change_pas": v_ok}
        out.append("- **{}** : verdict préenregistré → **{}** (baisse ≥ 0.30 : ii {}, iii {}, iv {} ; (v) stable : {}).".format(
            key, verdict, *["oui" if baisse[s] else "non" for s in ("ii", "iii", "iv")], "oui" if v_ok else "non"))

    # --- B
    out += ["", "## B — distracteur isolé (T1-A, attendu `contradiction`)", "",
            "| cas | distracteur | choix (P du choix) par appel | P(contradiction) par appel | médiane | tue la contradiction (< 0.5) | P(E > D) médiane |",
            "|---|---|---|---|---|---|---|"]
    js["B"] = {}
    for cid, lab in (("A1-i", "aucun (T1-A, = A1-i)"), ("B-FAIT", "fait redondant A > C (= L-DIS1 E006)"),
                     ("B-FAIT2", "fait redondant B > D"), ("B-REGLE", "règle 3 non pertinente seule"),
                     ("B-NEUTRE", "fait couleur(A, rouge) seul"), ("A1-v", "phrase hors sujet ajoutée (A1-v)")):
        rs = sel(ev, cid, "statut")
        m = med([e["p"] for e in rs])
        me = med([e["p"] for e in sel(ev, cid, "e_sup_d")])
        out.append("| {} | {} | {} | {} | {} | {} | {} |".format(cid, lab, choix(rs), ps(rs), f2(m),
                                                                 "—" if m is None else ("**oui**" if m < 0.5 else "non"), f2(me)))
        js["B"][cid] = {"mediane_p_contradiction": m, "tue": None if m is None else m < 0.5, "p_e_sup_d": me}

    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "analyse.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    (HERE / "results" / "analyse.json").write_text(json.dumps(js, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
