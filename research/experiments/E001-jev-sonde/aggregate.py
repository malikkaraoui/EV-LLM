#!/usr/bin/env python3
"""E001 -- agregation de plusieurs lancements de run.py (Python standard, zero dependance).

Usage :
  python3 aggregate.py --cases cases-T2.json results/<h1> results/<h2> ...

- lit, dans chaque dossier, raw.public.jsonl (sinon raw.jsonl) ;
- ne garde que les appels HTTP 200 ;
- verifie que chaque appel garde correspond bien au cas de --cases (meme state, memes
  questions) : on n'agrege jamais des appels faits sur des attentes differentes ;
- ecrit results/agregat-<horodatage>/summary.json + summary.md, au MEME format que run.py.

La regle conforme / faux et sur n'est pas reimplementee : summarize() et summary_md()
sont ceux de run.py, importes tels quels.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run  # noqa: E402  (summarize, summary_md : regle inchangee)


def read_records(run_dir):
    """Retourne (nom du fichier lu, liste des lignes) pour un dossier de lancement."""
    run_dir = Path(run_dir)
    for name in ("raw.public.jsonl", "raw.jsonl"):
        path = run_dir / name
        if path.is_file():
            lines = path.read_text(encoding="utf-8").splitlines()
            return name, [json.loads(l) for l in lines if l.strip()]
    raise FileNotFoundError("ni raw.public.jsonl ni raw.jsonl dans {}".format(run_dir))


def aggregate(cases, run_dirs):
    """Retourne (rows, meta_partielle). Leve ValueError si un appel ne correspond pas aux cas."""
    by_id = {c["id"]: c for c in cases}
    kept, sources = [], []
    for d in run_dirs:
        name, recs = read_records(d)
        statuts = {}
        for r in recs:
            s = str(r.get("http_status"))
            statuts[s] = statuts.get(s, 0) + 1
        sources.append({"dossier": Path(d).name, "fichier": name, "n_appels": len(recs),
                        "statuts_http": statuts})
        for r in recs:
            if r.get("http_status") != 200:
                continue
            case = by_id.get(r.get("case_id"))
            if case is None:
                continue
            body = r.get("request_body") or {}
            if body.get("state") != case["state"] or body.get("questions") != case["questions"]:
                raise ValueError("{} / {} rep {} : requete differente du cas de --cases".format(
                    Path(d).name, r.get("case_id"), r.get("rep")))
            kept.append(r)
    rows = run.summarize(cases, kept)
    return rows, {"sources": sources, "n_http_200": len(kept),
                  "n_appels": sum(s["n_appels"] for s in sources)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--out-root", default=str(HERE / "results"))
    ap.add_argument("run_dirs", nargs="+")
    args = ap.parse_args(argv)

    cases_bytes = Path(args.cases).read_bytes()
    cases = json.loads(cases_bytes.decode("utf-8"))["cases"]
    try:
        rows, part = aggregate(cases, args.run_dirs)
    except (ValueError, FileNotFoundError) as e:
        print("ERREUR : {}".format(e), file=sys.stderr)
        return 2

    run_id = "agregat-" + datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    out_dir = Path(args.out_root) / run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    meta = {"run_id": run_id, "endpoint": run.ENDPOINT, "model": run.MODEL,
            "reps": "agregat de {} lancements (HTTP 200 seulement)".format(len(args.run_dirs)),
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
            "n_appels": part["n_appels"], "n_http_200": part["n_http_200"],
            "sources": part["sources"]}
    (out_dir / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (out_dir / "summary.md").write_text(run.summary_md(rows, meta), encoding="utf-8")
    print("agregat : {}".format(out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
